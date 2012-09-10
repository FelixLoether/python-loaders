import sys
from peak.util.proxies import ObjectWrapper, ObjectProxy

from loaders import Lazy


class TestLazyLoader(object):
    def setup_method(self, method):
        self.name = '%s.pkg.module' % __package__
        self.loader = Lazy(self.name, ['attr1', 'attr2'])

    def teardown_method(self, method):
        if self.name in sys.modules:
            del sys.modules[self.name]
        sys.meta_path.remove(self.loader)

    def test_find_module_finds_module(self):
        assert self.loader.find_module(self.name, '') is self.loader

    def test_find_module_does_not_find_others(self):
        assert self.loader.find_module('pkg.modal', '') is None
        assert self.loader.find_module('pkg', '') is None
        assert self.loader.find_module('module', '') is None
        assert self.loader.find_module('some.module', '') is None
        assert self.loader.find_module('a.b', '') is None

    def test_load_module_returns_from_sys_modules_if_present(self):
        module = object()
        sys.modules[self.name] = module
        assert self.loader.load_module(self.name) is module

    def test_load_module_returns_cahced_module_when_already_loaded(self):
        module = object()
        self.loader.loaded = True
        self.loader.module = module
        assert self.loader.load_module(self.name) is module
        assert sys.modules[self.name] is module

    def test_load_module_creates_module_on_first_load_and_caches_it(self):
        module = self.loader.load_module(self.name)
        assert isinstance(module, ObjectWrapper)
        assert self.loader.module is module
        assert sys.modules[self.name] is module

    def test_create_lazy_module_creates_object(self):
        obj = self.loader.create_lazy_module()
        assert isinstance(obj, ObjectWrapper)
        assert hasattr(obj, 'attr1')
        assert isinstance(obj.attr1, ObjectProxy)
        assert hasattr(obj, 'attr2')
        assert isinstance(obj.attr2, ObjectProxy)

    def test_import_before_ready_gives_proxy_with_none_values(self):
        from pkg import module
        assert isinstance(module, ObjectWrapper)
        assert module.__subject__ is None
        assert module.attr1.__subject__ is None
        assert module.attr2.__subject__ is None
        assert not hasattr(module, 'attr3')

    def test_import_after_ready_gives_proxy_with_real_values(self):
        import pkg.module as module
        self.loader.ready()
        assert isinstance(module, ObjectWrapper)
        assert module.__subject__ is not None
        assert module.attr1 == 1
        assert module.attr2 == 2
        assert module.attr3 == 3
