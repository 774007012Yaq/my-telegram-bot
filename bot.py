import os # <-- مهم جداً لاستخدام متغيرات البيئة
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ... (بقية الكود من الأعلى كما هو بدون تغيير) ...
# --- نسخ ولصق بقية الكود هنا ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def build_menu(buttons, n_cols):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    return menu

def get_main_menu_keyboard():
    buttons = [
        InlineKeyboardButton("📚 عرض المواد", callback_data='show_materials'),
        InlineKeyboardButton("ℹ️ معلومات عنا", callback_data='about_us'),
        InlineKeyboardButton("🕒 عرض الوقت والتاريخ", callback_data='show_time'),
    ]
    return InlineKeyboardMarkup(build_menu(buttons, 2))

def get_back_keyboard():
    buttons = [
        InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='main_menu')
    ]
    return InlineKeyboardMarkup(build_menu(buttons, 1))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"أهلاً بك يا {user.first_name} في بوت المساعد العلمي!\n\nاستخدم الأزرار أدناه للتنقل."
    await update.message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    callback_data = query.data

    if callback_data == 'main_menu':
        text = "أنت في القائمة الرئيسية. اختر ما تريد:"
        await query.edit_message_text(text=text, reply_markup=get_main_menu_keyboard())
    elif callback_data == 'show_materials':
        text = "هنا ستظهر قائمة المواد الدراسية. (هذه ميزة يمكنك بناؤها لاحقاً)\n\n"
        await query.edit_message_text(text=text, reply_markup=get_back_keyboard())
    elif callback_data == 'about_us':
        text = "هذا البوت تم تطويره لمساعدة الطلاب في الوصول للمحتوى العلمي بسهولة.\n\n"
        text += "تم التطوير بواسطة: عمادالدين © 2025"
        await query.edit_message_text(text=text, reply_markup=get_back_keyboard())
    elif callback_data == 'show_time':
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = f"الوقت والتاريخ الحالي هو:\n{now}"
        await query.edit_message_text(text=text, reply_markup=get_back_keyboard())

# --- الدالة الرئيسية لتشغيل البوت ---
def main():
    """الدالة الرئيسية التي تقوم بتشغيل البوت."""
    
    # =================================================================
    #   <<< الطريقة الآمنة والصحيحة للاستضافة على الإنترنت >>>
    #   هذا الكود يقرأ التوكن من متغير بيئة اسمه BOT_TOKEN
    # =================================================================
    TOKEN = os.environ.get("BOT_TOKEN")

    if not TOKEN:
        logger.error("خطأ: لم يتم العثور على متغير البيئة BOT_TOKEN. يرجى تعيينه.")
        return

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("البوت قيد التشغيل...")
    application.run_polling()

if __name__ == '__main__':
    main()