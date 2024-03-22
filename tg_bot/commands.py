from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


class Commands:
    async def __start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        context.user_data["chat_session"] = []

        await update.message.reply_text("I'm a AI bot, please talk to me!")

    async def __new_session(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        context.user_data["chat_session"] = []

        if len(context.args) and context.args[0] == "system":
            await update.message.reply_text("Enter a hint for the bot")
            context.user_data["waiting_for_message"] = True

    def handlers(self):
        return [
            CommandHandler("start", self.__start),
            CommandHandler("new_session", self.__new_session),
        ]
