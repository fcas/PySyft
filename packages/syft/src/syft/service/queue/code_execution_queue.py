
from ...serde.deserialize import _deserialize as deserialize
from ...serde.serializable import serializable
from .base_queue import AbstractMessageHandler
from ...client.api import SyftAPICall
from .queue_stash import Status
from .queue_stash import QueueItem
from ..response import SyftError

import sys

@serializable()
class CodeExecutionMessageHandler(AbstractMessageHandler):
    queue_name = "code_execution"
    
    @staticmethod
    def handle_message(message: bytes):
        
        from ...node.node import Node
        # Interactions with the node:
        #   * fetching code_object
        #   * fetching policies
        #   * updating output policy state
        #   * updating action store with the result
        print("QUEUE:", file=sys.stderr)
        
        
        # task_uid, promised_result_id, code_item, filtered_kwargs, worker_setrtings = deserialize(message, from_bytes=True)
        
        task_uid, code_item_id, kwargs, worker_settings, user_verify_key = deserialize(message, from_bytes=True)
        print(worker_settings.document_store_config.client_config, file=sys.stderr)
        
        # worker.api.call(code_item.id, ...)
        
        worker = Node(
            id=worker_settings.id,
            name=worker_settings.name,
            signing_key=worker_settings.signing_key,
            document_store_config=worker_settings.document_store_config,
            action_store_config=worker_settings.action_store_config,
            blob_storage_config=worker_settings.blob_store_config,
            is_subprocess=True,
        )

        item = QueueItem(
            node_uid=worker.id,
            id=task_uid,
            status=Status.PROCESSING,
        )
        worker.queue_stash.set_placeholder(user_verify_key, item)
        print("Queue Stash data:", worker.queue_stash.partition.data)

        status = Status.COMPLETED
        
        call = SyftAPICall(
            node_uid=worker.id, path="code.call", args=[code_item_id], kwargs=kwargs, blocking=True
        )
        signed_call = call.sign(worker_settings.signing_key)
        try:
            result = worker.handle_api_call(signed_call)
            if isinstance(result, SyftError):
                status = Status.ERRORED
        except Exception as e:  # nosec
            status = Status.ERRORED
            result = SyftError(message=f"Failed with exception: {e}")
        
        deser_msg = deserialize(result.serialized_message, from_bytes=True)
        
        item = QueueItem(
            node_uid=worker.id,
            id=task_uid,
            result=result,
            resolved=True,
            status=status,
        )

        worker.queue_stash.set_result(worker.verify_key, item)
        print("Done. Sanity check:", deser_msg.data.get(), file=sys.stderr)
        print("Queue Stash data:", worker.queue_stash.partition.data)
            