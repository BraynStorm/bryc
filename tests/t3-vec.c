/* bryc: start
from t3 import *

declare_vectors(['char', 'int'])
*/
#define VECTOR static inline
struct vector_char
{
    char* data;
    size_t size;
    size_t capacity;
};
VECTOR char vector_char_get(struct vector_char* _v, int index)
{
    return _v->data[index];
}
VECTOR char vector_char_set(struct vector_char* _v, int index)
{
    return _v->data[index];
}

struct vector_int
{
    int* data;
    size_t size;
    size_t capacity;
};
VECTOR int vector_int_get(struct vector_int* _v, int index)
{
    return _v->data[index];
}
VECTOR int vector_int_set(struct vector_int* _v, int index)
{
    return _v->data[index];
}

#define vector_get(VEC, IND) _Generic((VEC), \
    struct vector_char*: vector_char_get,\
    struct vector_int*: vector_int_get,\
)(VEC, IND)

#undef VECTOR
/* bryc: end */

int main() { return 0; }