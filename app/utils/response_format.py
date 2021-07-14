class ResponseFormat:
    '''
    This is the response object used across all endpoints for both success and error response
    '''
    def __init__(self, message, data, status) -> None:
        self.message = message
        self.data = data
        self.status = status

    def toObject(self):
        return {
            'message': self.message,
            'status': self.status,
            'data': self.data
        }