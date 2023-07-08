from bryc import bryc

from dataclasses import dataclass


@dataclass
class Vector:
    dtype: str

    @property
    def name(self) -> str:
        return "vector_" + self.dtype.replace(" ", "_").replace("*", "_ptr")

    def declaration_struct(self) -> str:
        return f"""struct {self.name}
{{
    {self.dtype}* data;
    size_t size;
    size_t capacity;
}};"""

    def declaration_functions(self) -> str:
        return f"""
VECTOR {self.dtype} {self.name}_get(struct {self.name}* _v, int index)
{{
    return _v->data[index];
}}
VECTOR {self.dtype} {self.name}_set(struct {self.name}* _v, int index)
{{
    return _v->data[index];
}}
"""

    def declaration(self) -> str:
        return self.declaration_struct() + self.declaration_functions()


def declare_generic_macros(vectors: list[Vector]) -> str:
    o = ""
    o += "#define vector_get(VEC, IND) _Generic((VEC), \\\n"
    for v in vectors:
        o += f"    struct {v.name}*: {v.name}_get,\\\n"
    o = o[:-2] + "\\\n)(VEC, IND)\n"
    return o


def declare_vectors(types: list[str]):
    vecs = {t: Vector(t) for t in types}
    bryc().emit("#define VECTOR static inline")
    for t, v in vecs.items():
        bryc().emit(v.declaration())
    bryc().emit(declare_generic_macros(list(vecs.values())))
    bryc().emit("#undef VECTOR")
