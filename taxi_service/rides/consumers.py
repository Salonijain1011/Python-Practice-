
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class RideTrackingConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.ride_id = self.scope['url_route']['kwargs'].get('ride_id')
#         if not self.ride_id:
#             await self.close()  
#             return

#         await self.channel_layer.group_add(f"ride_{self.ride_id}", self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         if hasattr(self, "ride_id"):  
#             await self.channel_layer.group_discard(f"ride_{self.ride_id}", self.channel_name)

#     async def receive(self, text_data):
#         try:
#             data = json.loads(text_data)
#             latitude = data.get("latitude")
#             longitude = data.get("longitude")

#             if latitude is None or longitude is None:
#                 await self.send(text_data=json.dumps({"error": "Invalid data format"}))
#                 return

#             await self.channel_layer.group_send(
#                 f"ride_{self.ride_id}", {
#                     "type": "send_ride_update",
#                     "latitude": latitude,
#                     "longitude": longitude,
#                     "ride_id": self.ride_id,
#                 }
#             )

#         except json.JSONDecodeError:
#             await self.send(text_data=json.dumps({"error": "Malformed JSON"}))

#     async def send_ride_update(self, event):
#         await self.send(text_data=json.dumps(event))


import json
from channels.generic.websocket import AsyncWebsocketConsumer

def parse_json(text_data):
    try:
        return json.loads(text_data)
    except json.JSONDecodeError:
        return {"error": "Malformed JSON"}

def validate_location_data(data):
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    if latitude is None or longitude is None:
        return {"error": "Invalid data format"}
    return {"latitude": latitude, "longitude": longitude}

class RideTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs'].get('ride_id')
        if not self.ride_id:
            await self.close()  
            return

        await self.channel_layer.group_add(f"ride_{self.ride_id}", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "ride_id"):  
            await self.channel_layer.group_discard(f"ride_{self.ride_id}", self.channel_name)

    async def receive(self, text_data):
        data = parse_json(text_data)

        if "error" in data:
            await self.send(text_data=json.dumps(data))
            return

        validated_data = validate_location_data(data)
        if "error" in validated_data:
            await self.send(text_data=json.dumps(validated_data))
            return

        await self.broadcast_ride_update(validated_data)

    async def broadcast_ride_update(self, validated_data):
        await self.channel_layer.group_send(
            f"ride_{self.ride_id}",
            {
                "type": "send_ride_update",
                "latitude": validated_data["latitude"],
                "longitude": validated_data["longitude"],
                "ride_id": self.ride_id,
            }
        )

    async def send_ride_update(self, event):
        await self.send(text_data=json.dumps(event))
