from aiogram.dispatcher.filters.state import State, StatesGroup


class NewBuy(StatesGroup):
    GoogId = State()
    Promo = State()
    Paying = State()

class SuppUser(StatesGroup):
    UserId = State()

class AddPromo(StatesGroup):
    Promo = State()

class SuppAdmin(StatesGroup):
    UserId = State()
    QuestId = State()
    Text = State()

class NewFaq(StatesGroup):
    Name = State()
    Text = State()
    Photo = State()

class FaqName(StatesGroup):
    FaqId = State()
    Name = State()

class FaqText(StatesGroup):
    FaqId = State()
    Text = State()

class AddCatRus(StatesGroup):
    CatName = State()

class ChangeNamecatRus(StatesGroup):
    CatId = State()
    CatName = State()

class AddSubcatRus(StatesGroup):
    CatId = State()
    SubcatName = State()

class ChangeNamesubcatRus(StatesGroup):
    SubcatId = State()
    SubcatName = State()

class AddGood(StatesGroup):
    SubcatId = State()
    CatId = State()
    Name = State()
    Description = State()
    Photo = State()
    Price = State()

class AddInstance(StatesGroup):
    GoodId = State()
    FileName = State()

class ChangeNameGoodRus(StatesGroup):
    GoodId = State()
    GoodName = State()

class ChangeDescGoodRus(StatesGroup):
    GoodId = State()
    GoodDesc = State()

class ChangePriceGood(StatesGroup):
    GoodId = State()

class NewOrder(StatesGroup):
    Delivery = State()
    Adress = State()
    Comment = State()
    Promo = State()

class OrderEnd(StatesGroup):
    OrderId = State()

class RassilkaAll(StatesGroup):
    Text = State()

class ChangeToken(StatesGroup):
    Paym = State()
    Token = State()

class ChangeStatus(StatesGroup):
    UserId = State()

class ChangeRules(StatesGroup):
    Rules = State()

class ReviewTake(StatesGroup):
    OrderId = State()
    Stars = State()
    Review = State()

class QuestAddQuest(StatesGroup):
    CountMsg = State()
    QuestId = State()

class ChangeReviewPay(StatesGroup):
    Pay = State()

class NewUsername(StatesGroup):
    Username = State()

class ChageNicknameAdm(StatesGroup):
    UserId = State()
    Nickname = State()