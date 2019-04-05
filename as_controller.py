import requests

def as_controller (
    cls,
    ip,
    port = 8080, ## TODO: User credentials or keys?
):
    '''
        Return the given class acting as a
        controller for a remote version of
        itself at the given ip on the given port.
    '''
    class new_class (cls):
        '''
            The new class to be returned.
        '''
        __REMOTE_IP = ip
        __REMOTE_PORT = port

        def __on_remote (
            self,
            method,
            **kwargs,
        ):
            '''
                Run the given method on the
                remote class with the given kwargs.
            ''' ## TODO: Controlling remote instance not class...
            result = requests.post ( ## TODO: self.__base__ won't work as you'll need to know the remote instance name?
                'http://' + self.__REMOTE_IP + ':' + self.__REMOTE_PORT + '/' + self.__base__ + '/' + method,
                json = kwargs,
            )
            if (result.status_code != 200):
                raise AttributeError () ## TODO: Use / proxy the given error codes and/or messages?
            return result.json ()['data']

        def __getattribute__ (self, name): ## TODO: REVIEW: Think this also covers __setattr__.
            '''
                Call methods on the remote class.
                For variable / attribute access, set
                method to __getattribute__,
            '''
            local_result = super ().__getattribute__ (name)
            if not callable (local_result):
                return self.__on_remote (
                    method = '__getattribute__',
                    kwargs = {'name': name},
                )

            def new_callable (**kwargs):
                '''
                    Return a method that instead runs
                    the named method on the remote
                    class when called.
                '''
                return self.__on_remote (
                    method = name,
                    **kwargs,
                )

            return new_callable

    return new_class
