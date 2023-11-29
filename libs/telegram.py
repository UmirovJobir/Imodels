import telebot

from django.urls import reverse
from django.conf import settings

from telebot.util import quick_markup

from libs.sms import client

bot = telebot.TeleBot(settings.MYSERVICE.get('telebot').get('token'))


def return_markup(id, request):
    admin_url = reverse('admin:index')
    full_admin_url = request.build_absolute_uri(admin_url)
    return quick_markup({
        # "🟡 Yangi": {'callback_data': f'new|{id}'},
        # "🟢 To'langan": {'callback_data': f'paid|{id}'},
        # "🔴 Rad etilgan": {'callback_data': f'rejected|{id}'},
        # "☑️ Yetkazib berildi": {'callback_data': f'closed|{id}'},
        f"Buyurtma: #{id}": {'url': f'{full_admin_url}shop/order/{id}/change/'},
    }, row_width=1)


def send_message(type=None, **kwargs):
    if type == "order":
        order = kwargs.get('order')
        request = kwargs.get('request')

        basket = ""
        pk = 1

        for product in order.order_products.all():
            if len(product.product_name) > 20:
                name = product.product_name[:20] + "..."
            else:
                name = product.product_name
            basket += f"{pk}. {name} ✖️ {product.quantity}dona\n💵{product.subtotal:,.2f}\n"
            pk += 1

        if order.status == "Yangi":
            order_status = "🟡 " + order.status
        elif order.status == "To'langan":
            order_status = "🟢 " + order.status
        elif order.status == "Rad etilgan":
            order_status = "🔴 " + order.status

#💳 Метод оплата: Наличными при получении
#📅 Дата: {order.created_at.strftime("%d.%m.%Y, %H:%M")}
# 💸 Status: {order_status}
        telegram_message = f"""
📩 Yangi buyurtma❗️\n
📄 ID: #{order.pk}
-----------------------
👤 Mijoz:  {order.customer.first_name} {order.customer.last_name}
📞 Raqam: <code>+{order.customer.phone}</code>
-----------------------
{basket}-----------------------
💰 Jami: {order.total_price:,.2f} UZS
"""
        

# 💸 Status:\n{order_status}
        sms_message = f"""📄 Buyurtma: #{order.pk}
-----------------------
{basket}-----------------------
💰 Jami: {order.total_price:,.2f} UZS"""
        
        chat_id = settings.MYSERVICE.get('telebot').get('chat_id').get('chat_id_orders')

        try:
            bot.send_message(chat_id=chat_id,
                                text=telegram_message,
                                reply_markup= return_markup(id=order.pk, request=request),
                                parse_mode="HTML")
            # if settings.DEBUG==False:
            #     client._send_sms(
            #         phone=order.customer.phone,
            #         code=sms_message)
        except:
            pass
    
    elif type == "auth":
        try:
            bot.send_message(chat_id=chat_id, text=kwargs.get('text'), parse_mode="HTML")
        except:
            pass
    
    elif type == "contact":
        obj = kwargs.get('obj')
        
        telegram_message = f"""
📩 Yangi murojaat❗️\n
👤 Mijoz:  {obj.name}
📧 Email: {obj.email}
📞 Raqam: <code>+{obj.phone}</code>
📄 Xabar:  <code>{obj.message}</code>
"""
        chat_id = settings.MYSERVICE.get('telebot').get('chat_id').get('chat_id_warnings')

        try:
            # contact_request_markup = quick_markup({
            #     '✅': {'callback_data': f'contact_answered|{obj.pk}'},
            #     '❌': {'callback_data': f'contact_rejected|{obj.pk}'},
            # })
            bot.send_message(chat_id=chat_id,
                             text=telegram_message,
                             parse_mode="HTML",
                            #  reply_markup=contact_request_markup
                             )
        except:
            pass
