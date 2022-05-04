from pydantic import BaseModel


def sanitize_sqlalchemy_or_pydantic(object):
    """
    :param object: SQLAlchemy object
    :return: Sanitized SQLAlchemy object
    """
    if isinstance(object, BaseModel):
        return object.dict(exclude_unset=True)

    object = object.__dict__.copy()
    filtered_object = {k: v for k, v in object.items() if v is not None}
    return filtered_object
