from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Item, Base

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user


# Menu for UrbanBurger
category1 = Category(name="Basketball")

session.add(category1)
session.commit()

category2 = Category(name="Soccer")

session.add(category2)
session.commit()

category3 = Category(name="Baseball")

session.add(category3)
session.commit()

category4 = Category(name="Frisbee")

session.add(category4)
session.commit()

category5 = Category(name="Snowboarding")

session.add(category5)
session.commit()

category6 = Category(name="Rock Clibming")

session.add(category6)
session.commit()

category7 = Category(name="Football")

session.add(category7)
session.commit()

category8 = Category(name="Skating")

session.add(category8)
session.commit()

item1 = Item(title="basketball", description="A spherical inflated ball used in basketball games. Basketballs typically range in size from very small promotional items only a few inches in diameter to extra large balls nearly a foot in diameter used in training exercises. For example, a basketball in high school would be about 27 centimetres (cm) in circumference, while an NBA ball would be about 29 cm. The actual standard size of a basketball in the NBA is 29.5 cm in circumference", category=category1, user_id=1)

session.add(item1)
session.commit()

item2 = Item(title="basketball hoop", description="Horizontal circular metal hoop supporting a net through which players try to throw the basketball", category=category1, user_id=1)

session.add(item2)
session.commit()

item3 = Item(title="soccer ball", description="A round object that is kicked around often times covered in white and black hexagons.", category=category2, user_id=1)

session.add(item3)
session.commit()

item4 = Item(title="goal", description="A physical structure or area where an attacking team must send the ball in order to score points", category=category2, user_id=1)

session.add(item4)
session.commit()

item5 = Item(title="baseball", description='The ball features a rubber or cork center, wrapped in yarn, and covered, in the words of the Official Baseball Rules "with two strips of white horsehide or cowhide, tightly stitched together."', category=category3, user_id=1)

session.add(item5)
session.commit()

item6 = Item(title="baseball bat", description="A smooth wooden or metal club used in the sport of baseball to hit the ball after it is thrown by the pitcher.", category=category3, user_id=1)

session.add(item6)
session.commit()

item7 = Item(title="frisbee", description="A brand of plastic concave disk, used for various catching games by sailing it between two or more players and thrown by making it spin as it is released with a flick of the wrist.", category=category4, user_id=1)

session.add(item7)
session.commit()

item8 = Item(title="snowboard", description="A board for gliding on snow, resembling a wide ski, to which both feet are secured and that one rides in an upright position", category=category5, user_id=1)

session.add(item8)
session.commit()

item9 = Item(title="rock climbing wall", description="An artificially constructed wall with grips for hands and feet, usually used for indoor climbing, but sometimes located outdoors.", category=category6, user_id=2)

session.add(item9)
session.commit()

item10 = Item(title="chalk", description="A loose powder in a special chalk bag designed to prevent spillage, most often closed with a drawstring", category=category6, user_id=2)

session.add(item10)
session.commit()

item11 = Item(title="football", description="A ball with pointed ends inflated with air that is used to play one of the various sports known as football", category=category7, user_id=2)

session.add(item11)
session.commit()

item12 = Item(title="cones", description="A plastic shape that has a circle at the bottom and sides that narrow to a point used to help in drills and exercises.", category=category7, user_id=2)

session.add(item12)
session.commit()

item13 = Item(title="skateboard", description="It usually consists of a specially designed maplewood board combined with a polyurethane coating used for making smoother slides and stronger durability along with trucks and wheels", category=category8, user_id=2)

session.add(item13)
session.commit()




print "added items!"