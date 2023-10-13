
#ifndef __BOX_CORE_TYPE__
#define __BOX_CORE_TYPE__

#define T_BOX_NULL          0x00ui8
#define T_BOX_BYTE          0x01ui8
#define T_BOX_INT           0x02ui8
#define T_BOX_FLOAT         0x03ui8
#define T_BOX_SIZE          0x04ui8
#define T_BOX_ASCII         0x05ui8
#define T_BOX_TAG           0x06ui8
#define T_BOX_STR           0x07ui8
#define T_BOX_DATA          0x08ui8

#define T_BOX_ITEM          0x0eui8
#define T_BOX_TABLE         0x0fui8
#define T_BOX_TYPE          0xffui8

#define T_BOX_INT8          0x10ui8
#define T_BOX_UINT8         0x18ui8
#define T_BOX_INT16         0x11ui8
#define T_BOX_UINT16        0x19ui8
#define T_BOX_INT64         0x12ui8
#define T_BOX_UINT64        0x1Aui8


typedef signed char         box_int8;
typedef unsigned char       box_uint8;
typedef signed short        box_int16;
typedef unsigned short      box_uint16;
typedef signed long long    box_int64;
typedef unsigned long long  box_uint64;

typedef unsigned char       box_byte;
typedef signed long long    box_int;
typedef float               box_float;

#define MAX_BOX_BYTE        255ui8
#define MIN_BOX_BYTE        0ui8
#define MAX_BOX_INT         9223372036854775807i64
#define MIN_BOX_INT         (-9223372036854775808i64)


typedef size_t              box_size;
typedef char                box_ascii;
typedef char                box_tag [16];
typedef char                box_str [256];

#define LEN_BOX_TAG         16ui8
#define LEN_BOX_STR         255ui8

typedef struct box_data
{
    box_size size;
    box_byte data[];
} box_data;

typedef struct box_item
{
    box_tag tag;
    box_type type;
    box_byte value[];
};

typedef struct box_table
{
    box_byte count;
    box_byte items[];
} box_table;



typedef enum box_type
{
    t_box_null              = T_BOX_NULL,
    t_box_byte              = T_BOX_BYTE,
    t_box_int               = T_BOX_INT,
    t_box_float             = T_BOX_FLOAT,
    t_box_size              = T_BOX_SIZE,
    t_box_ascii             = T_BOX_ASCII,
    t_box_tag               = T_BOX_TAG,
    t_box_str               = T_BOX_STR,
    t_box_data              = T_BOX_DATA,
    t_box_int8              = T_BOX_INT8,
    t_box_uint8             = T_BOX_UINT8,
    t_box_int16             = T_BOX_INT16,
    t_box_uint16            = T_BOX_UINT16,
    t_box_int64             = T_BOX_INT64,
    t_box_uint64            = T_BOX_UINT64,
    t_box_item              = T_BOX_ITEM,
    t_box_table             = T_BOX_TABLE,
    t_box_type              = T_BOX_TYPE,
} box_type;



#endif /* __BOX_CORE_TYPE__ */
