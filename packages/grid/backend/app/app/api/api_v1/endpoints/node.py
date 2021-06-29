import json
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.db.session import engine, SessionLocal
from syft.core.node.common.tables import Base
from syft.core.node.common.tables.utils import seed_db
from syft import Domain

router = APIRouter()

from syft.core.common.message import (
    SignedImmediateSyftMessageWithoutReply,
    SignedImmediateSyftMessageWithReply,
)

import syft as sy

domain = sy.Domain("my domain", db_engine=engine)
Base.metadata.create_all(engine)
seed_db(SessionLocal())

@router.get("/", response_model=str)
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    if crud.user.is_superuser(current_user):
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return "hello world"


@router.get("/metadata", response_model=str)
def syft_metadata():
    return Response(domain.get_metadata_for_client()._object2proto().SerializeToString(), media_type="application/octet-stream")




@router.post("/pysyft", response_model=str)
async def syft(
    request: Request,
#    domain: Domain = Depends(deps.get_db),
#    skip: int = 0,
#    limit: int = 100,
#    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    data = await request.body()
    obj_msg = sy.deserialize(blob=data, from_bytes=True)
    if isinstance(obj_msg, SignedImmediateSyftMessageWithReply):
        reply = domain.recv_immediate_msg_with_reply(msg=obj_msg)
        r = Response(sy.serialize(obj=reply, to_bytes=True), media_type="application/octet-stream")
        return r
    elif isinstance(obj_msg, SignedImmediateSyftMessageWithoutReply):
        domain.recv_immediate_msg_without_reply(msg=obj_msg)
    else:
        domain.recv_eventual_msg_without_reply(msg=obj_msg)
    return ""
