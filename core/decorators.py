import functools
import logging
from exceptions import AWSError
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)

def handles_aws_error(func):

    @functools.wraps(func)
    def wrapper(*args,**kwargs):

        try:
            return func(*args,**kwargs)
        except ClientError as e:
            code  = e.response["Error"]["Code"]
            logger.error(f"AWS error en : {func.__name__} : {code}",exc_info=True)
            raise AWSError(code=code)
    return wrapper