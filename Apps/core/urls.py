from django.urls import path
from . import (CircleViews, UcViews, itemCategoryViews, stockItemViews, postViews, ChairmanViews, BankViews)
from .utils import loadMessage
app_name = 'core'

urlpatterns = [
    

    # Circle Paths
    path('circle/add/', CircleViews.CircleAddView.as_view(), name="circleAdd"),
    path('circle/list/', CircleViews.CircleListView.as_view(), name="circleList"),
    path('circle/search/', CircleViews.CircleSearchView.as_view(), name="circleSearch"),
    path('circle/<slug:name>/Update/', CircleViews.CircleUpdateView.as_view(), name="circleUpdate"),
    path('circle/<slug:name>/Delete/', CircleViews.CircleDeleteView.as_view(), name="circleDelete"),
    
    # Uc Paths
    path('uc/list/', UcViews.UcListView.as_view(), name="ucList"),
    path('uc/Add/', UcViews.UcCreateView.as_view(), name="ucAdd"),
    path('uc/search/', UcViews.UcSearch.as_view(), name="ucSearch"),
    path('uc/<str:name>/Update/', UcViews.UcUpdateView.as_view(), name="ucUpdate"),
    path('uc/<str:name>/Delete/', UcViews.UcDeleteView.as_view(), name="ucDelete"),
    
    # Item Category  Paths
    path('item-Category/list/', itemCategoryViews.ItemCategoryList.as_view(), name="itemCategoryList"),
    path('item-Category/add/', itemCategoryViews.ItemCategorAddView.as_view(), name="itemCategoryAdd"),
    path('item-Category/search/', itemCategoryViews.itemCategorySearchView.as_view(), name="itemCategorySearch"),
    path('item-Category/<str:name>/Update/', itemCategoryViews.ItemCategorUpdateView.as_view(), name="itemCategoryUpdate"),
    path('item-Category/<str:name>/Delete/', itemCategoryViews.itemCategoryDeleteView.as_view(), name="itemCategoryDelete"),
    
    
    # Item Category  Paths
    path('stock-Item/list/', stockItemViews.StockItemListView.as_view(), name="stockItemList"),
    path('stock-Item/add/', stockItemViews.StockItemCreateView.as_view(), name="stockItemAdd"),
    path('stock-Item/search/', stockItemViews.stockItemSearch.as_view(), name="stockItemSearch"),
    path('stock-Item/<str:name>/Update/', stockItemViews.stockItemUdateView.as_view(), name="stockItemUpdate"),
    path('stock-Item/<str:name>/Delete/', stockItemViews.stockItemDeleteView.as_view(), name="stockItemDelete"),

    # Post Views
    path('post/list/', postViews.postListView.as_view(), name="postList"),
    path('post/add/', postViews.postCraeteView.as_view(), name="postAdd"),
    path('post/search/', postViews.postSearchView.as_view(), name="postSearch"),
    path('post/<str:name>/<str:bps>/Update/',postViews.postUdateView.as_view(), name="postUpdate"),
    path('post/<int:pk>/Delete/', postViews.postDeleteView.as_view(), name="postDelete"),


    # Bank Paths
    path('bank/add/', BankViews.bankAddView.as_view(), name="bankAdd"),
    path('bank/list/', BankViews.bankListView.as_view(), name="bankList"),
    path('bank/search/', BankViews.bankSearchView.as_view(), name="bankSearch"),
    path('bank/<slug:name>/Update/', BankViews.bankUpdateView.as_view(), name="bankUpdate"),
    path('bank/<slug:name>/Delete/', BankViews.bankDeleteView.as_view(), name="bankDelete"),
    
    
    
    # Bank Paths
    path('chairman/add/', ChairmanViews.chairmanAddView.as_view(), name="chairmanAdd"),
    path('chairman/list/', ChairmanViews.chairmanListView.as_view(), name="chairmanList"),
    path('chairman/search/', ChairmanViews.chairmanSearchView.as_view(), name="chairmanSearch"),
    path('chairman/<slug:name>/Update/', ChairmanViews.chairmanUpdateView.as_view(), name="chairmanUpdate"),
    path('chairman/<slug:name>/Delete/', ChairmanViews.chairmanDeleteView.as_view(), name="chairmanDelete"),
    

    # Extra
    path("message/load/", loadMessage, name="message")
    
]

