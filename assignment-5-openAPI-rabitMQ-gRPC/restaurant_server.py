from concurrent import futures

import grpc
import sys
from proto import restaurant_pb2
from proto import restaurant_pb2_grpc

RESTAURANT_ITEMS_FOOD = ["chips", "fish", "burger", "pizza", "pasta", "salad"]
RESTAURANT_ITEMS_DRINK = ["water", "fizzy drink", "juice", "smoothie", "coffee", "beer"]
RESTAURANT_ITEMS_DESSERT = ["ice cream", "chocolate cake", "cheese cake", "brownie", "pancakes", "waffles"]

class Restaurant(restaurant_pb2_grpc.RestaurantServicer):
    # Logic goes here
    def FoodOrder(self, request_iterator, context):
        food_order_id = request_iterator.orderID
        food_order_items = request_iterator.items
        food_order_status = restaurant_pb2.RestaurantResponse.Status.ACCEPTED
        for i in food_order_items:
            if i not in RESTAURANT_ITEMS_FOOD:
                food_order_status = restaurant_pb2.RestaurantResponse.Status.REJECTED
        return restaurant_pb2.RestaurantResponse(orderID=food_order_id, status=food_order_status)
    def DrinkOrder(self, request_iterator, context):
        drink_order_id = request_iterator.orderID
        drink_order_items = request_iterator.items
        drink_order_status = restaurant_pb2.RestaurantResponse.Status.ACCEPTED
        for i in drink_order_items:
            if i not in RESTAURANT_ITEMS_DRINK:
                drink_order_status = restaurant_pb2.RestaurantResponse.Status.REJECTED
        return restaurant_pb2.RestaurantResponse(orderID=drink_order_id, status=drink_order_status)
    def DessertOrder(self, request_iterator, context):
        dsrt_order_id = request_iterator.orderID
        dsrt_order_items = request_iterator.items
        dsrt_order_status = restaurant_pb2.RestaurantResponse.Status.ACCEPTED
        for i in dsrt_order_items:
            if i not in RESTAURANT_ITEMS_DESSERT:
                dsrt_order_status = restaurant_pb2.RestaurantResponse.Status.REJECTED
        return restaurant_pb2.RestaurantResponse(orderID=dsrt_order_id, status=dsrt_order_status)
def serve():
    # Logic goes here
    # Remember to start the server on localhost and a port defined by the first command line argument
    port = sys.argv[1]
    localhost = 'localhost:{0}'.format(port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    restaurant_pb2_grpc.add_RestaurantServicer_to_server(Restaurant(), server)
    server.add_insecure_port(localhost)
    server.start()
    server.wait_for_termination()
if __name__ == '__main__':
    serve()
