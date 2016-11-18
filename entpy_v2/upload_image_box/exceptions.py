# list of custom exceptions with error code

class CorruptedImageUIBError(Exception):
    """Error in image upload, file may be corrupted"""
    get_error_code = "001"
    pass

class ImageSizeUIBError(Exception):
    """Image size wrong"""
    get_error_code = "002"
    pass

class ImageDimensionsUIBError(Exception):
    """Image height or width wrong"""
    get_error_code = "003"
    pass

class ImageExtensionUIBError(Exception):
    """Image extension wrong"""
    get_error_code = "004"
    pass
