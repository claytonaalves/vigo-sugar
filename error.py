def custom500(err):
    return repr(type(err))

handler = {
    500: custom500,
}
