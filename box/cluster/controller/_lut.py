

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from threading import Lock
from time import time
from typing import Any

from box.common.resources._resource import Resource



LUT_MODIFY_INTERVAL = 0.1
UPDATE_MAX_WORKERS = 1
LUT_THREAD_POOL_UPDATE = ThreadPoolExecutor(max_workers=UPDATE_MAX_WORKERS)



@dataclass
class LutNode():
    resource        : Resource
    max_life        : float
    nodes           : dict                  = field(default_factory=dict)
    parent          : Any                   = None
    last_modified   : float                 = field(default_factory=time)
    modify_lock     : Lock                  = field(default_factory=Lock)

    def __post_init__(self):
        self.resource = (
            Resource(**self.resource)
            if isinstance(self.resource, dict)
            else self.resource
        )
        for key, node in self.nodes:
            self.nodes[key] = (
                LutNode(**node)
                if isinstance(node, dict)
                else node
            )
    

    def is_alive(self):
        self.max_life > time()


    def query(self, path):
        path = path.split("/")
        _result = []
        _node = self

        while path and _node:
            _res = _node.resource
            if not _res is None and _res.is_alive():
                _result.append(_res)
            _key, path = path[ :1 ], path[ 1: ]
            while path and not _key:
                _key, path = path[ :1 ], path[ 1: ]
            _node = _node.nodes.get(_key, None)
        
        LUT_THREAD_POOL_UPDATE.submit(_node.update)
        return _result
    
    
    def insert(self, path, res):
        path = path.split("/")
        _life = res.life()
        _now = time()
        _node = self
        _key, path = path[ :1 ], path[ 1: ]
        _ret = False

        while path and not _key:
            _key, path = path[ :1 ], path[ 1: ]

        while _key:
            _next = None
            with _node.modify_lock:
                if _key in _node.nodes:
                    _next = _node.nodes[_key]
                else:
                    _next = LutNode(None, parent=_node)
                _node.last_modified = _now
                _node.max_life = max(_life, _node.max_life)
            _key, path = path[ :1 ], path[ 1: ]
            while path and not _key:
                _key, path = path[ :1 ], path[ 1: ]
            _node = _next
            
        with _node.modify_lock:
            if _node.resource is None:
                _node.resource = res
                _node.last_modified = _now
                _node.max_life = max(_life, _node.max_life)
                _ret = True
            elif (_node.resource.timestamp < res.timestamp
            and _node.resource.life() < res.life()):
                _node.resource = res
                _node.last_modified = _now
                _node.max_life = max(_life, _node.max_life)
                _ret = True
        
        LUT_THREAD_POOL_UPDATE.submit(_node.update)
        return _ret


    def update(self):
        _now = time()
        _node = self

        while _node:

            if _now - _node.last_modified < LUT_MODIFY_INTERVAL:
                return
            
            with _node.modify_lock:
                _max_life = 0
                _dead_nodes = []
                if not _node.resource is None:
                    if _node.resource.life() < _now:
                        _node.resource = None
                    else:
                        _max_life = max(_max_life, _node.resource.life())
                for key in _node.nodes:
                    if _node.nodes[key].max_life < _now:
                        _dead_nodes.append(key)
                    else:
                        _max_life = max(_max_life, _node.nodes[key].max_live)
                for key in _dead_nodes:
                    _node.nodes.pop(key)
                _node.last_modified = _now
                _node.max_life = _max_life
            
            _node = _node.parent
    
