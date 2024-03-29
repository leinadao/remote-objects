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
    key_given = request.json.pop (
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
            return dict (
                data = to_call (**request.json),
            )
        return abort (404, 'Method not found.')
    return abort (404, 'Object not found.')

run (
    host = '192.168.1.67',
    port = 8080,
)
