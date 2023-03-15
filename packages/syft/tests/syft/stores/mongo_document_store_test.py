# stdlib
from threading import Thread

# syft absolute
from syft.core.node.new.document_store import PartitionSettings
from syft.core.node.new.document_store import QueryKeys
from syft.core.node.new.mongo_client import MongoStoreClientConfig
from syft.core.node.new.mongo_document_store import MongoStoreConfig
from syft.core.node.new.mongo_document_store import MongoStorePartition

# relative
from .store_mocks_test import MockObjectType
from .store_mocks_test import MockSyftObject


def test_mongo_store_partition_sanity(
    mongo_store_partition: MongoStorePartition,
) -> None:
    res = mongo_store_partition.init_store()
    assert res.is_ok()

    assert hasattr(mongo_store_partition, "_collection")


def test_mongo_store_partition_init_failed() -> None:
    # won't connect
    mongo_config = MongoStoreClientConfig(connectTimeoutMS=1, timeoutMS=1)

    store_config = MongoStoreConfig(client_config=mongo_config)
    settings = PartitionSettings(name="test", object_type=MockObjectType)

    store = MongoStorePartition(settings=settings, store_config=store_config)

    res = store.init_store()
    assert res.is_err()


def test_mongo_store_partition_set(mongo_store_partition: MongoStorePartition) -> None:
    res = mongo_store_partition.init_store()
    assert res.is_ok()

    obj = MockSyftObject(data=1)

    res = mongo_store_partition.set(obj, ignore_duplicates=False)

    assert res.is_ok()
    assert res.ok() == obj
    assert len(mongo_store_partition.all().ok()) == 1

    res = mongo_store_partition.set(obj, ignore_duplicates=False)
    assert res.is_err()
    assert len(mongo_store_partition.all().ok()) == 1

    res = mongo_store_partition.set(obj, ignore_duplicates=True)
    assert res.is_ok()
    assert len(mongo_store_partition.all().ok()) == 1

    obj2 = MockSyftObject(data=2)
    res = mongo_store_partition.set(obj2, ignore_duplicates=False)
    assert res.is_ok()
    assert res.ok() == obj2
    assert len(mongo_store_partition.all().ok()) == 2

    for idx in range(100):
        obj = MockSyftObject(data=idx)
        res = mongo_store_partition.set(obj, ignore_duplicates=False)
        assert res.is_ok()
        assert len(mongo_store_partition.all().ok()) == 3 + idx


def test_mongo_store_partition_delete(
    mongo_store_partition: MongoStorePartition,
) -> None:
    res = mongo_store_partition.init_store()
    assert res.is_ok()

    objs = []
    for v in range(100):
        obj = MockSyftObject(data=v)
        mongo_store_partition.set(obj, ignore_duplicates=False)
        objs.append(obj)

    assert len(mongo_store_partition.all().ok()) == len(objs)

    # random object
    obj = MockSyftObject(data="bogus")
    key = mongo_store_partition.settings.store_key.with_obj(obj)
    res = mongo_store_partition.delete(key)
    assert res.is_err()
    assert len(mongo_store_partition.all().ok()) == len(objs)

    # cleanup store
    for idx, v in enumerate(objs):
        key = mongo_store_partition.settings.store_key.with_obj(v)
        res = mongo_store_partition.delete(key)
        assert res.is_ok()
        assert len(mongo_store_partition.all().ok()) == len(objs) - idx - 1

        res = mongo_store_partition.delete(key)
        assert res.is_err()
        assert len(mongo_store_partition.all().ok()) == len(objs) - idx - 1

    assert len(mongo_store_partition.all().ok()) == 0


def test_mongo_store_partition_update(
    mongo_store_partition: MongoStorePartition,
) -> None:
    mongo_store_partition.init_store()

    # add item
    obj = MockSyftObject(data=1)
    mongo_store_partition.set(obj, ignore_duplicates=False)
    assert len(mongo_store_partition.all().ok()) == 1

    # fail to update missing keys
    rand_obj = MockSyftObject(data="bogus")
    key = mongo_store_partition.settings.store_key.with_obj(rand_obj)
    res = mongo_store_partition.update(key, obj)
    assert res.is_err()

    # update the key multiple times
    for v in range(10):
        key = mongo_store_partition.settings.store_key.with_obj(obj)
        obj_new = MockSyftObject(data=v)

        res = mongo_store_partition.update(key, obj_new)
        assert res.is_ok()

        # The ID should stay the same on update, unly the values are updated.
        assert len(mongo_store_partition.all().ok()) == 1
        assert mongo_store_partition.all().ok()[0].id == obj.id
        assert mongo_store_partition.all().ok()[0].id != obj_new.id
        assert mongo_store_partition.all().ok()[0].data == v

        stored = mongo_store_partition.get_all_from_store(QueryKeys(qks=[key]))
        assert stored.ok()[0].data == v


def test_mongo_store_partition_set_multithreaded(
    mongo_store_partition: MongoStorePartition,
) -> None:
    thread_cnt = 5
    repeats = 100
    mongo_store_partition.init_store()

    execution_err = None

    def _kv_cbk(tid: int) -> None:
        nonlocal execution_err
        for idx in range(repeats):
            obj = MockObjectType(data=idx)
            res = mongo_store_partition.set(obj, ignore_duplicates=False)

            if res.is_err():
                execution_err = res
            assert res.is_ok(), res

    tids = []
    for tid in range(thread_cnt):
        thread = Thread(target=_kv_cbk, args=(tid,))
        thread.start()

        tids.append(thread)

    for thread in tids:
        thread.join()

    assert execution_err is None
    stored_cnt = len(mongo_store_partition.all().ok())
    assert stored_cnt == thread_cnt * repeats


def test_mongo_partition_update_multithreaded(
    mongo_store_partition: MongoStorePartition,
) -> None:
    thread_cnt = 5
    repeats = 100

    obj = MockSyftObject(data=0)
    key = mongo_store_partition.settings.store_key.with_obj(obj)
    mongo_store_partition.set(obj, ignore_duplicates=False)
    execution_err = None

    def _kv_cbk(tid: int) -> None:
        nonlocal execution_err
        for repeat in range(repeats):
            obj = MockSyftObject(data=repeat)
            res = mongo_store_partition.update(key, obj)

            if res.is_err():
                execution_err = res
            assert res.is_ok(), res

    tids = []
    for tid in range(thread_cnt):
        thread = Thread(target=_kv_cbk, args=(tid,))
        thread.start()

        tids.append(thread)

    for thread in tids:
        thread.join()

    assert execution_err is None


def test_mongo_partition_set_delete_multithreaded(
    mongo_store_partition: MongoStorePartition,
) -> None:
    thread_cnt = 5
    repeats = 100
    execution_err = None

    def _kv_cbk(tid: int) -> None:
        nonlocal execution_err
        for idx in range(repeats):
            obj = MockSyftObject(data=idx)
            res = mongo_store_partition.set(obj, ignore_duplicates=False)

            if res.is_err():
                execution_err = res
            assert res.is_ok()

            key = mongo_store_partition.settings.store_key.with_obj(obj)

            res = mongo_store_partition.delete(key)
            if res.is_err():
                execution_err = res
            assert res.is_ok(), res

    tids = []
    for tid in range(thread_cnt):
        thread = Thread(target=_kv_cbk, args=(tid,))
        thread.start()

        tids.append(thread)

    for thread in tids:
        thread.join()

    assert execution_err is None
    stored_cnt = len(mongo_store_partition.all().ok())
    assert stored_cnt == 0
