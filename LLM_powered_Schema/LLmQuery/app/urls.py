from django.urls import path
from .views import chatbot_response, home, chatbot_response_api,chatbot_response_graph,graph

urlpatterns = [
    path("", home, name="home"),
    path("chatbot-response/", chatbot_response, name="chatbot_response"),
     path('chatbot/', chatbot_response_api, name='chatbot_response'),
     path('graph/', graph, name='chatbot_response'),
      path("chatbot_graph/", chatbot_response_graph, name="chatbot_response_for_graph"),
]
