from bottle import (
    abort,
    request,
    route,
    run,
)

key = 'u9f349uca0jd0jf0594j09sd09420fnrdnfuhf9ojsoedcIOmf'

@route ('/<object>/<method>')
def handle (object, method): ## TODO: Correct methods POST, GET etc?
    '''
        Handle a request.
    '''
    kwargs = request.json (kwargs)
    key_given = kwargs.pop (
        'key',
        None,
    )
    if not key_given == key:
        abort (401, 'Invalid key.')
    to_call_on = globals ().get (
        object,
        None,
    )
    if to_call_on:
        to_call = getattr (
            to_call_on,
            method,
            None,
        )
        if to_call:
            kwargs = request.json (kwargs)
            return dict (
                data = to_call (**kwargs),
            )
        return abort (404, 'Method not found.')
    return abort (404, 'Object not found.')
