from sanic import Blueprint, Request, HTTPResponse, json

from db import Database
from model import Item

item = Blueprint("item", url_prefix="/item")


@item.get('/list')
async def _list_items(request: Request) -> HTTPResponse:
    return json(dict([pair async for pair in Database.get_instance().list_items()]))


@item.post('/')
async def _new_item(request: Request) -> HTTPResponse:
    _id = await Database.get_instance().add_item(Item.from_dict(request.json))
    return json({
        "id": _id,
        "item": request.json,
    })


@item.get('/<item_id>')
async def _get(request: Request, item_id: int) -> HTTPResponse:
    try:
        i = await Database.get_instance().get_item(item_id)
    except KeyError:
        return json({}, status=404)
    return json(i)


@item.patch('/<item_id>')
async def _update(request: Request, item_id: int) -> HTTPResponse:
    try:
        await Database.get_instance().update_item(item_id, request.json)
    except KeyError:
        return json({}, status=404)
    return json(request.json)


@item.post('/<item_id>/delete')
async def _delete(request: Request, item_id: int) -> HTTPResponse:
    try:
        await Database.get_instance().delete_item(item_id, request.json.get("reason", "No removal reason provided"))
    except KeyError:
        return json({}, status=404)
    return json({})


@item.put('/<item_id>/restore')
async def _restore(request: Request, item_id: int) -> HTTPResponse:
    try:
        await Database.get_instance().undelete(item_id)
    except KeyError:
        return json({}, status=404)
    return json({})
