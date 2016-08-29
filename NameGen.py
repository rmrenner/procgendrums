import random

class NameType:
	def __init__(self, name_template, *word_types):
		self.name_template = name_template
		self.word_types = word_types

	def generate_name(self):
		words = []
		for c in self.word_types:
			s = random.choice(c)
			c.remove(s)
			words.append(s)
		return self.name_template.format(*words)

adjectives = ['Wet', 'Glamorous', 'Sexy', 'Urban', 'Helpless', 'Intimate', 'Mild', 'Fake', 'Dense', 'Morbid', 'Funny', 'Awful', 'Crisp', 'Cold', 'Hot', 'False', 'True', 'Young', 'Infinite', 'Shaky', 'Permanent', 'Ancient', 'Nasty', 'Sick', 'Delicate', 'Deep', 'Dry', 'Fuzzy', 'Long', 'Unique', 'Old', 'Electric', 'Healing', 'Redemptive', 'Effervescent', 'Ecstatic', 'Cute']
cloth_types = ['Satin', 'Cotton', 'Silk', 'Gingham', 'Burlap', 'Organza', 'Suede', 'Vinyl', 'Polyester', 'Denim']
colors = ['Black', 'White', 'Grey', 'Pink', 'Silver', 'Gold', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Indigo', 'Violet']
garments = ['Shorts', 'Pants', 'Hotpants', 'Skirt', 'Miniskirt', 'Gown', 'Party Dress', 'Long-Sleeved Shirt', 'Short-Sleeved Shirt', 'Breeches', 'Tube Top', 'Jacket']
nouns = ['Desire', 'Forest', 'Grace', 'Hate', 'Legend','Love', 'Mask','Milk','Murder','Poise','Problem', 'Shadow','Statesman', 'Cakes', 'Cookie', 'Quake', 'Stories', 'Box', 'Man', 'Morning', 'Magician', 'Tower', 'Genius', 'Beauty', 'Rifle', 'Decay', 'Game', 'Life', 'Day', 'Night', 'Guest', 'Girl', 'Face', 'Handbook', 'Diary', 'Justice', 'Crime', 'Thought', 'Warmth', 'Depth', 'Light', 'Seed', 'Swerve', 'Envy', 'Germs', 'Burn', 'Lips', 'Eyes', 'Midnight', 'Queen']


nfs = [] # Name Formats.

nfs.append(NameType("{} & {}", adjectives, adjectives)) #Wet & Glamorous
nfs.append(NameType("{}, {}, {}", adjectives, adjectives, adjectives)) #Wet, Glamorous, Sexy
nfs.append(NameType("{} {}", adjectives, cloth_types)) #
nfs.append(NameType("{} {}", adjectives, colors))
nfs.append(NameType("{} {}", adjectives, garments))
nfs.append(NameType("{} {}", adjectives, nouns))

def generate():
    return random.choice(nfs).generate_name()
