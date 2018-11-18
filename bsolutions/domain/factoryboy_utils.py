# factoryboy_utils.py

@classmethod
def _get_manager(cls, model_class):
    return super(cls, cls)._get_manager(model_class).using(cls.database)


class DBAwareFactory(object):
    """
    Context manager to make model factories db aware

    Usage:
        with DBAwareFactory(PersonFactory, 'db_qa') as personfactory_on_qa:
            person_on_qa = personfactory_on_qa()
            ...
    """
    def __init__(self, cls, db):
        # Take a copy of the original cls
        self.original_cls = cls
        # Patch with needed bits for dynamic db support
        setattr(cls, 'database', db)
        setattr(cls, '_get_manager', _get_manager)
        # save the patched class
        self.patched_cls = cls

    def __enter__(self):
        return self.patched_cls

    def __exit__(self, type, value, traceback):
        return self.original_cls
