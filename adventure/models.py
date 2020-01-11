from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
import uuid
import random

QUALITY_NAMES = ['Thrash', 'Broken', 'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Supreme']

MATERIAL_NAMES = {'Acoustium': ['Acoustium', 'Acoustium is a fictional metal featured in the episode Shriek of the Batman Beyond series. Acoustium was found in a metal alloy of a sonic device able to generate sound waves potent enough to demolish whole buildings. It"s not clear what acoustium exactly does, except increasing the acoustic properties when included in a metallic alloy.'],
'Adamantium': ['Adamantium', 'Used in various fantasy/science fiction settings; see main article'],
'Administratium': ['Administratium', 'Slows down chemical reactions; a reaction normally complete in less than a second will take several days in its presence. This element is a joke, a spoof on the bureaucracy of scientific establishments and on descriptions of newly discovered elements.'],
'Afraidium': ['Afraidium', 'The robot Fender claims to be made of this metal. "It"s yellow," he states, "and tastes like chicken."'],
'Agricite': ['Agricite', 'It is a metal mineral that occurs in the ground and is mined outside of MegaKat City. It is incredibly strong and is used to make hardened objects like tanks. Implied to something, it annotates strength.'],
'Alkahest': ['Alkahest', 'A powerful substance, most known as "universal solvent", which could dissolve everything. It was sought in alchemy. But it could never exist, as if it dissolves everything, it would be impossible to place it in a container.'],
'AM2': ['AM2', 'Anti-matter mineral from parallel universe (only known to Emperor), the unique energy source that provides all power needs of mankind and the Earth Empire.'],
'Amazonium': ['Amazonium', 'Found only on the island of Themyscira, this metal is used in alloys to create extremely strong and lightweight armor. An example of an Amazonium alloy is found in Wonder Woman"s bracelets.'],
'Arcanite': ['Arcanite', 'A dull, flexible metal that can be forged to an edge sharper than iron and steel.'],
'Atmosphereum (also often spelled as "Atmospherium")': ['Atmosphereum (also often spelled as "Atmospherium")', 'An extremely rare element, abundant in outer space, which among many other uses is a power source and capable of raising the dead. If obtained and researched, it would certainly have countless benefits for Science! Not to be confused with an Amish Terrarium.'],
'Axonite': ['Axonite', 'A "miracle substance" in the Dr. Who universe. Axonite is a "thinking" molecule that can replicate any substance. Axonite, in the end, turns out to be a malevolent element that intends to spread itself across the cosmos in order to feed itself.'],
'Balthazate': ['Balthazate', 'A Crystallic material found beneath the shiverpeaks. Balthazate looks similar to Quartz crystals roughly half the size of a man. It is a highly potent explosive as shown when four crystal brought down a large portion of a cave when ignited.'],
'Balthorium': ['Balthorium', 'A fictional element used in the Russians" doomsday device. It is possible that this is a mispronunciation on the part of actor Peter Bull of the words "Cobalt-Thorium G," as both (real) elements can be used in atomic weapons to increase the amount of dangerous nuclear fallout, which agrees with the sense in which "Balthorium" is used in the movie.'],
'Basidiumite (also Brumblium)': ['Basidiumite (also Brumblium)', 'A slightly greenish solid, twice the density of uranium. Infragreen spectrum. Makes up the blue-green planet Basidium.'],
'Bazoolium': ['Bazoolium', 'A gold-coloured metal that can predict the weather.'],
'Beerium': ['Beerium', 'Splitting the Beerium atom infuses the beer with bubbles.'],
'Bendezium': ['Bendezium', 'An extremely tough metal that can only be destroyed by a power bomb.'],
'Beresium': ['Beresium', 'An asteroid which hit the Terra Nova colony contained this geological element. This impact created a "poison rain" which killed many colonists and drove the rest underground.'],
'Bernalium': ['Bernalium', 'Evidentially a conductive material, given its use in a high-energy weapon system. It gets its name from J. D. Bernal, a British physicist.'],
'Blingidium': ['Blingidium', '"The rarest compound in the universe". A large statue made of this substance in the shape of Topato is dug up by Wigu"s family. Touching it leads to a feeling of ecstasy ("feeling light" and "tasting watermelon"). It is destroyed by the Space Mummy.'],
'Bolonium or Bolognium': ['Bolonium or Bolognium', 'A fictional element used to describe something as impossible or nonsensical: "Your explanations are pure, weapons-grade bolonium!" According to Oscar Mayer"s promotional periodic table of elements in The Simpsons, the atomic weight of bolonium is "delicious" or "snacktacular".'],
'Byzantium': ['Byzantium', 'A highly powerful radioactive element transported in a safe aboard the sunken RMS Titanic.'],
'Caesiumfrankolithicmixialubidiumrixidixidexidoxidroxide': ['Caesiumfrankolithicmixialubidiumrixidixidexidoxidroxide', 'A chemical famous in its era, it was the cure for a virus that was eating away at the hulls of the mining ship, Red Dwarf. Arnold Rimmer retrieved the name of the chemical, taking two hours to recite its long name. It is not to be confused with Caesiumfrankolithicmixialubidiumrixidexidixidoxidroxide (note that "dixidexi" is changed to "dexidixi"), which is a completely different compound.'],
'Calculon': ['Calculon', 'Discovered by Professor Cuthbert Calculus. This substance has a silicon base and can resist very high temperatures. It was one of the scientific discoveries that enabled Professor Calculus to plan a manned mission to the Moon.'],
'Capitalium': ['Capitalium', '"Comprised of a cloud of entreprenions, which are attracted to a core of opportunium, which was made stable by emissions from Governmentium." See also Administratium.'],
'Capsidium': ['Capsidium', 'Creates energy during planetary conjunctions if the lights hit the Capsidium, used by Krang and Shredder to power the Technodrome.'],
'Carbonite': ['Carbonite', 'Carbonite was originally used to keep Tibanna gas fresh. The chamber on Bespin was reconfigured to provide stasis for Luke Skywalker for his transport to Emperor Palpatine. It was tested on Han Solo. It was then used to transport criminals.'],
'Carmot': ['Carmot', 'This term was used by alchemists for a mythological element which the Philosopher"s stone is said to be made of. Both things could maybe be the same.'],
'Cavorite': ['Cavorite', 'Cavorite is impervious to gravity and can shield other materials from its effects. It is used to shield a craft from Earth"s pull, allowing easy flight. It was named after its discoverer, Dr Cavor, who used its levitational properties to travel to the Moon. It also coats Martian flying machines, although it is referred to as a "gravity-blocking substance", and not Cavorite.'],
'Chelonium': ['Chelonium', 'A material which according to the Unseen University wizards mostly makes up the world-bearing turtle "Great A"Tuin." Since they can do a test to determine its (non)existence in Roundworld they are probably correct.'],
'Chemical X': ['Chemical X', 'When Professor Utonium was creating the Power Puff Girls, he accidentally added this chemical to the mixture of sugar, spice and everything nice. It is responsible for the girls" super powers.'],
'Chromedigizoid': ['Chromedigizoid', 'A digital metal alloy, present in many Digimon as armor or weapons.'],
'Chronoton': ['Chronoton', 'Associated with manipulating or traveling through time in Star Trek, as well as in Futurama. A chroniton bomb in Teen Titans destroys chronitons in a given area, stopping that area"s progression through time. A "Chroniton Rifle" is the most powerful weapon in Jets"n"Guns.'],
'Claudia': ['Claudia', 'An element used to power vanships and larger airships. It glows a light blue and is found naturally in solid form. However, while in liquid form, it generates an anti-gravity field when put through certain processes, which allows the aforementioned ships to fly. Its solid form is also used as a unit of currency, simply called a claudia.'],
'Colour out of space': ['Colour out of space', 'Toxic and mutagenic element, of indescribable colour and unknown spectrum, from a meteorite that lands in a field.'],
'Corbomite': ['Corbomite', 'Fictional within the fictional Star Trek universe. The non-existent substance was named by Captain James T. Kirk as part of a bluff to prevent the destruction of the Starship Enterprise by another vessel. The material and device (both were called "corbomite" in the bluff) would supposedly redirect any destructive energy back to its source, destroying the attacker. The material has since appeared in various other series and video games set in the Star Trek universe.'],
'Corrodium': ['Corrodium', 'An alien element that is capable of mutating certain lifeforms. Prolonged exposure is required for the mutations to be permanent.'],
'Cortexrulestheworldium': ['Cortexrulestheworldium', 'At the end of the game during the credit sequence, It says that Doctor Neo Cortex discovered a new element in the periodic table, and was warned against naming it Cortexrulestheworldium.'],
'Dalekanium': ['Dalekanium', 'A metal used by the Daleks as a component of their armoured casings. Originally called polycarbide, but dubbed Dalekanium by a human. Also, in an alternate reality, an unstable explosive powerful enough to penetrate those casings. The two may not be the same substance.'],
'Deletium': ['Deletium', 'An unwanted substance typically removed from computer systems. Characterized by consistent performance failures and expensive upgrades. Also, any Microsoft product.'],
'Destronium': ['Destronium', 'A liquid that helps Cybertronians repair themselves. It is plentiful on Cybertron but on Earth, humans were only able to synthesize small samples. At high speeds, destronium can get very volatile and would take out half a city the size of Detroit if it detonates.'],
'Diamondillium': ['Diamondillium', 'A substance harder than anything in this universe. The only substance that rivals its hardness is diamondium, though odds are it may be the same substance under a different name.'],
'Diamondium': ['Diamondium', 'A substance harder than anything in this universe. The only substance that rivals its hardness is diamondillium, though odds are it may be the same substance under a different name.'],
'Dilithium': ['Dilithium', 'A fictional crystalline mineral in the universe of Star Trek that is used to regulate the anti-matter-powered warp drives that allow starships to travel faster than light.'],
'Disgruntium': ['Disgruntium', 'An element which attracts and absorbs all levity, humor, and joy. It is highly toxic on direct contact but also radiates an unknown particle or field which affects the emotional state of nearby individuals.'],
'Dragonbane': ['Dragonbane', 'A mineral which is poisonous to dragons. It is the material that the legendary Dragon Blade is made of.'],
'Duetronium': ['Duetronium', 'A material is a flammable liquid with many uses.The Robinsons spent much of their time drilling for deutronium, as they required it as fuel for the Jupiter 2.It often appears like small,white pebbles,that is refined by either drilling or pumping out of the ground.The Robinsons store,Duetronium in small ,silver plastic bottles.The name possibly is a combination of Deuterium and possibly Plutonium or Nuetromiun .Some species consumed deutronium as food, including the Cyclamen and the People of the Green Mist . (" Attack of the Monster Plants ", " Wild Adventure ")'],
'Dwarfstar Alloy/Hull Metal': ['Dwarfstar Alloy/Hull Metal', 'Ships hulls from various sci-fi novels starting in the 1920"s were said to be built using this ultra-strong material. It was said to be an extremely condensed state of matter, ie. Neutron Star material, and used as a plot device to make nearly invunerable ships without having to invent some implassible new materials.'],
'Element 152': ['Element 152', 'Element created by Mon-El by combining gold, silver and iron. It has anti-gravity properties and was eventually used in rings, allowing members of the Legion of Super-Heroes to fly.'],
'Element X': ['Element X', 'Element of extraterrestrial origin that, when combined with a precise mixture of terrestrial iron ore at high temperatures, has enough explosive capacity to destroy an entire solar system.'],
'Element Zero': ['Element Zero', 'Also known as eezo, this is generated when solid matter is affected by the energy of a star going supernova. When subjected to an electrical current, it produces a field that increases or decreases the mass of an object. Used in a number of applications, the most noticeable being FTL travel. Humans exposed to this element while still in the womb may gain the ability to generate their own fields and are known as biotics.'],
'Elementium': ['Elementium', 'An element that came from the Elemental Plane, thus making it very rare. It is capable of channeling elemental energies. It is used to craft the Thunderfury, Blessed Blade of the Windseeker.'],
'Elephantanium': ['Elephantanium', 'Turns the one who contacts it into an elephant.'],
'Elephantigen': ['Elephantigen', 'A material which according to the Unseen University wizards makes up the four world-bearing elephants: Berilia, Tubul, Great T"phon and Jerakeen. Since they determine with a simple test that it does not exist in Roundworld they are probably correct.'],
'Elerium-115': ['Elerium-115', 'The element, atomic number 115, upon which all alien power systems are based. It facilitates space flight (although whether faster-than-light or not is not explicit) due to its property of emitting gravity waves under particle bombardment. Used as a fuel for advanced craft, and to power weapons and devices based on alien technology.'],
'Endurium': ['Endurium', 'Crystalline element discovered during an archeological dig powering an ancient starship. Subsequently used to power other starships based on the discovered starships technology. An entire planet comprised of the element is discovered moving through the galaxy triggering solar flares wiping out all life in the solar systems it passes through. Eventually the element is discovered to be a sentient life form.'],
'Energon': ['Energon', 'Highly radioactive, highly unstable material that can by synthesized through refinement of other materials (though the process to do this is unknown, and naturally-occurring Energon does exist). Energon can be either crystalline or liquid in form, and can appear in a variety of colors.'],
'Eridium': ['Eridium', 'A glowing purple element that arose in abundance on the planet Pandora after the first Eridian Vault (to which it gets it"s name) was opened by the Vault hunters in the first game of the series, to which it has multiple purposes, it is primarily used in the creation of E-Tech (Eridium-Tech) weapons, which can convert bullets into a whole myriad of devastating laser-like weapons, such as Railguns, Plasma Casters and BFGs; but also has a use in acting as a catalyst/boost for sirens (6 different women with varying mystic powers), at the cost of their own health, and can lead them to becoming reliant on a constant supply of the substance for them to even live. It"s by-product, known as "Slag" is highly toxic in many ways, to the extent where it can be weaponised to weaken a target"s defense, making them vulnerable to consecutive attacks, but ingesting Eridium or Slag causes slag-poisoning and horrific Slag mutation.'],
'Eternium': ['Eternium', 'An ore that is said to be a major source of magic power. Comes from only one location: the Rock of Eternity, the home of the wizard Shazam and guarded by all members of the Marvel family. The Rock was destroyed in the 30th century, causing the fourth Captain Marvel to search for the pieces. Following the explosion, however, Eternium proved to be harmful to her, in a manner comparable with Kryptonite"s effect on Kryptonians. Also referenced in World of Warcraft as the most difficult lockbox in the game, only dropped in high level dungeons and can only be opened by experienced lockpickers.'],
'Etherium': ['Etherium', 'A bright blue mineral present in small amounts in all rocks in the location Castle in the Sky takes place in. Pure crystals of etherium, which are very difficult to manufacture, are capable of repelling gravity to a degree, causing objects to float. It also stimulates plant growth.'],
'Explodium': ['Explodium', 'Extremely volatile element that is prone to massive releases of energy when even minutely disturbed. Most cars and most buildings used in film production are constructed from Explodium. This element is a joke, based on the tendency in movies for objects, especially cars, to explode much more often than they would in reality.'],
'Faidon': ['Faidon', 'Self-luminous blue crystals which are created out of crystallized energy in Supernova explosions and can only be wrought in the core of a white dwarf.'],
'Feminum': ['Feminum', 'Element found only on Paradise Island. Ore can be fashioned into a bulletproof metal, but is usually used for jewelry, such as bracelets.'],
'Finkilium': ['Finkilium', 'A rare metal sought by NASA and imperative to the success of the Saturn 12 program. Mentioned in episode 116, "Guess Who"s Going to Be A Bride".'],
'Froonium': ['Froonium', 'A substance created by series producer Richard Manning while he still worked on Star Trek to represent any esoteric material. Appeared in Farscape as an in-joke in several episodes. Manning"s Fandom nickname is "Froonium Ricky".'],
'Fulgarator/Deflagrator': ['Fulgarator/Deflagrator', 'An extremely powerful explosive developed by the literally mad scientist Thomas Roch in Jules Verne"s book and placed at the disposal of the pirate Ker Karaje. To produce an explosion the application of a liquid known as "Deflagrator" is needed, otherwise the Fulgarator is nothing but inert powder. A few grams suffice to smash a long tunnel through tough volcanic rock. A projectile powered by this explosive generates such shock waves as to destroy everything in a big radius all around. Several thousand tons would smash the entire Earth and render it into a new asteroid belt, though no one in the book is eager to go that far.'],
'Grimacite': ['Grimacite', 'This material is what one of the Kingdom"s two moons is made of. A chunk of it fell onto the Desert Beach after the moon, Grimace, was hit by a comet. The Penguin Mafia was using it for unknown purposes until the Naughty Sorceress made off with it.'],
'Gundanium Alloy': ['Gundanium Alloy', 'A material that is practically immutable, highly heat-resistant, and electrically neutral. The material also has the property of absorbing Electro-magnetic waves. These properties combine to produce a material that is extremely hard to damage, lending to the Gundams" atmosphere of invincibility and intimidation and highly stealthy. Additionally, heat and beam weapons produced using Gundanium are much stronger than similar weapons made using traditional titanium, thanks to its extremely high melting point and ability to absorb EM waves allowing it to produce hotter and therefore stronger beam energy without being damaged.'],
'Handwavium': ['Handwavium', 'Handwavium (as distinct from Unobtainium) is a substance used to violate the laws of physics or otherwise conveniently fill a plot hole without requiring effort on the part of the author. See "handwaving." Unobtainium, by contrast, is a substance that could (but is not known to) theoretically exist, or is impossible to obtain.'],
'Heavy Elements': ['Heavy Elements', 'Heavy elements are used to fuel Martian reactors, which seem to be the same as our nuclear reactors, although much smaller. It is presumably uranium, plutonium, or one or more even heavier elements'],
'Hellion': ['Hellion', 'The Hellion is a charged atom of Infernium. It is larger than you might think. And deadlier. Appears in-game as a monster made up of a single large (and deadly) atom which attacks by burning you with its particles ("He positively hits you with a proton. The overall effect for you is negative. Ouch! Ugh! Ugh!"). When defeated it will sometimes drop a "Hellion Cube" which is used to make "Hell Broth" much the same way a bouillon cube makes regular broth.'],
'Human': ['Human', 'Advertisements describe the "Human" element (#38, symbol "Hu", atomic mass 7E+09) to be the element of change. The Human element is the element that allows the advances in chemistry.'],
'Illudium Phosdex': ['Illudium Phosdex', 'Also known as the shaving cream atom, it was found only on Planet X, which was unfortunately destroyed when both Duck Dodgers and Marvin the Martian tried to conquer it for Earth and Mars, respectively.'],
'Illyrion': ['Illyrion', 'Valuable heavy element which the heroes must harvest from the centre of a star as it turns into a Nova.'],
'Imperium X': ['Imperium X', 'Highly inert element that does not annihilate when comes in contact with AM2. Is used to contain and store AM2.'],
'Impervium': ['Impervium', 'Material of which the doors of Scrooge McDuck"s money bin are made according to Carl Barks. Also, the material out of which darksteel is made. An element named impervium is also in the 1987 Teenage Mutant Ninja Turtles cartoon, used by Krang to power a force field generator. In Starbound, Impervium is and alloy of Rubium (a fictional red element found nly on threat level 9+ planets in the Starbound lore) and Carbon (found in Coal), and makes the best craftable equipment in the game.'],
'Imulsion': ['Imulsion', 'A liquid element discovered on the planet Sera. The idea to harness it as an energy source is the focus is the point of the pre-Emergence Day wars between the human colonies. When an unspecified amount of Imulsion was subliminated by the Lightmass bomb at the end of the first game in a major attack on the Locust Horde, the gas seeped into the atmosphere, resulting in a disease called "Rust Lung."'],
'Inertron': ['Inertron', 'Chemical element that is resistant to all known forms of chemical and electromagnetic interaction. It is essentially indestructible.'],
'Infernium': ['Infernium', 'Infernium ionizes to the Hellion. See Hellion. Additionally, Demoninjas sometimes brag about their katana blades being made of Infernium, so presumably the hot katana blades they sometimes leave behind are made of it too. Demoninjas claim that the blades are unbreakable, but this is demonstrably false; their most noteworthy property seems to be that they"re perpetually hot.'],
'Isogen': ['Isogen', 'Light-bluish crystal, formed by intense pressure deep within large asteroids and moons. Used in electronics and weapons manufacturing. Only found in abundance in a few areas.'],
'Japanium': ['Japanium', 'Extremely strong material used in the construction of Mazinger Z. Discovered by Doctor Tanaka. See also Super Alloy Z'],
'Jethrik': ['Jethrik', 'The rarest of elements, Jethrik (also spelled Jethryk) is found native as a blue mineral of incredible value. A few kilograms could "power a battlefleet for an entire campaign." In The Ribos Operation the Doctor and his assistant Romana retrieve the first Key to Time in its guise as a lump of the mineral.'],
'Jezz': ['Jezz', 'A fictional material featured in JezzBall. The object of the game is to contain the material by creating walls, until a percentage of the chamber is sealed.'],
'Jouronium': ['Jouronium', 'A material used to make sniper rifle bullets and other gun components.'],
'Jumbonium': ['Jumbonium', 'Each atom of this element is large enough to be easily visible to the naked eye, with marble-sized nucleons and electrons.'],
'Kairoseki': ['Kairoseki', 'Dull gray stone that nullifies the effects of Devil Fruits in the One Piece universe and weakens the Devil Fruit User. It can also be used to hide the presence of ships from sea monsters.'],
'Kryptonite': ['Kryptonite', 'Crystalline material, originally in various colours with separate effects, harmful to Kryptonians and created during the destruction of Superman"s home planet Krypton; synthesis is also possible. John Byrne"s retcon of the DC Comics universe established Green Kryptonite as a compound and later issues had experiments by Batman and Luthor reestablished the Pre-Crisis versions of Red, Blue, and Gold.'],
'Laconia': ['Laconia', 'Valuable metal used in the construction of weapons and armor, described as the strongest material in Algol. Found in great quantities on the planet Dezolis.'],
'Liquid electricity': ['Liquid electricity', 'The "distilled essence of electricity;" a glowing, liquid substance that provided fantastic energy and super-speed to vehicles, machines, and people.'],
'Lunar Titanium/Gundarium Alloy (Alpha, Beta, Gamma)': ['Lunar Titanium/Gundarium Alloy (Alpha, Beta, Gamma)', 'Lunar Titantium is an Titanium alloy that is manufactured in space and while having a perfect crystal structure, it also exhibits the properties of foam metal. It can take direct hits from a 120mm machine gun and survive unscratched for the first time that area got hit. It is also a material that is highly heat-resistant and can survive atmospheric reentry heat for around a certain period (but cannot survive the total duration of the reentry and needed other systems to assist it). It was originally named Lunar Titanium during the One Year War since it is manufactured in Lunar II, the asteroid base of the Earth Federation Forces. It was used in Gundam and thus after the war, the material was renamed as Gundarium Alloy Alpha when newer version named beta and gamma were developed.'],
'Lux': ['Lux', 'Material created from light; indestructible and transparent. Used in the hull of the heroes" spaceships. See also Relux.'],
'Maclarium': ['Maclarium', 'Mentioned in passing, Maclarium is a heavy element that has an atomic weight of over 200. No other details are given.'],
'Magicite': ['Magicite', 'A red-marked dark green crystal. Contains the magic and soul of a dead Esper.'],
'Maracite': ['Maracite', 'It is an element that can pass through water as easily as something could pass through air. It has an "inverted" way of corroding; it reacts fast with oxygen and carbon dioxide but stays unharmed if the oxygen is bonded to hydrogen.'],
'Marvelium': ['Marvelium', 'Invented by Captain Marvel"s nemesis, Sivana. Its atomic number is 99 (which has since been discovered and named Einsteinium)'],
'Megacyte': ['Megacyte', 'An extremely rare mineral found in comets and very occasionally in asteroids that have traveled through gas clouds. Has unique explosive traits that make it very valuable in the armaments industry.'],
'Meowium': ['Meowium', 'Atomic number 0. Primarily used as meowium dioxide (MeO2) which, when applied to the fur a cat, produces a voltage between areas of differently colored fur in the presence of sunlight.'],
'Metatron': ['Metatron', 'It serves functions similar to those of silicon, forming computer chips, but is much more advanced, capable of creating completely self-aware artificial intelligence. Also has space-compressing qualities in weapons and machinery, able to create pocket dimensions and allow faster travel from A to B by compressing the space in between.'],
'Mexallon': ['Mexallon', 'Very flexible metallic mineral, dull to bright silvery green in color. Can be mixed with Tritanium to make extremely hard alloys or it can be used by itself for various purposes. Fairly common in most regions.'],
'Minovsky Particle, Mega particle': ['Minovsky Particle, Mega particle', 'Minovsky Particles are two fictional particles (positive and negative Minovsky particle) found in the Universal Century that will form an I-Field when scattered in space. Depending on its density, it can block electro-magnetic waves and interfere with radar. Mega particle is a neutral version made by compressing the two Minovsky particles and used for powerful beam weaponry.'],
'Mithril': ['Mithril', 'A light, silvery metal ("mithril" means "true silver") that is extremely durable, but very light and easy to work. While mithril has properties similar to those of titanium or aluminium alloy, the fact that it was mined in native form in Moria suggests it has no direct real-world analogue. It is used for making superb chain-mail armour and other means of protection. It can also be worked into other forms (much as iron ore can be used to make various grades of iron and steel) with unusual properties (reflecting only the light of the moon, for instance). An alternate spelling, "Mythril", appears in the video game series Final Fantasy with basically the same properties as mithril. Also, "Mithral" used in D&D books to avoid copyright infringement claims, and "Milrith" in Simon the Sorcerer. In the Warhammer world, the High Elven metal "Ithilmar" has similar properties and usage.'],
'Mizzium': ['Mizzium', 'An alchemically potent, flameproof metal used in the experiments and devices of the Izzet League in the Guildpact expansion set. Its only appearance on cards is in the Mizzium Transreliquat, and the flavortext of Stomp and Howl. Other than that, its only other references are when mentioned in passing by members of the Creative department.'],
'Moonsilver': ['Moonsilver', 'The most protean of the five magical materials, can be formed where the light of the moon has boiled away the Wyld. Can be made to mimic muscle and nerves.'],
'Morphite': ['Morphite', 'Morphite is a highly unorthodox mineral that can only be found in the hard-to-get mercoxit ore. it is hard to use morphite as a basic building material, but when it is joined with existing structures it can enhance the performance and durability manifold. This astounding quality makes this the material responsible for ushering in a new age in technology breakthroughs.'],
'Naquadah': ['Naquadah', 'A dull grey heavy metal used by the Goa"uld and others as a power source, for the construction of Stargates, and in atomic weapons. The liquid Naquadah power-sources modules used in staff weapons glow fluorescent green. One isotope of Naquadah, Naquadriah, has similar properties but in a more extreme form. It is both more powerful and more unstable. (see below for Naquadriah)'],
'Narrativium': ['Narrativium', 'An element unique to the Discworld; proto-substance from which all things spring forth. It is the fundamental element of Story, and is how things know what they"re meant to be.'],
'Necrodermis': ['Necrodermis', 'A metal used by the Necrons to build their war machines and bodies. It heals and grows like an organism and has other unknown properties. Originally developed to serve as hulls for relativistic star ships which needed to resist the radiation of space. The C"tan use physical avatars made of this material.'],
'Necrogen': ['Necrogen', 'A material that exist solely on Mirrodin. In its natural state it"s a thick mist covering most parts of the Mephidross but can be crafted into a spellbomb for later use. It consumes metal and flesh, turning living creatures exposed to it for a long time into Nim, a kind of living zombie bent on consuming all that is not infected with necrogen. Mephidross vampires can use the necrogen mists to temporarily turn other creatures into vampires without harming them.'],
'Necronium': ['Necronium', 'A magical, radioactive metal, similar to Plutonium in all applications, save that it radiates oz particles, poisoning by which tends to cause the victim to join the undead. It is produced artificially in nuclear reactors analogous to Pu. Depleted Necronium is dense metal devoid of all magic, very toxic to magical creatures.'],
'Neoteutonium': ['Neoteutonium', 'A powerful energy source gifted to the Nazis by the mysterious Babel Syndicate, hoping to turn the tide of World War II.'],
'Neutrotope': ['Neutrotope', 'In the episode Mission to Destiny agents from the planet Destiny, plagued by a fungus killing of the world"s plant life, are transporting a prism made of Neutrotope which they have mortgaged their planet to purchase. The substance can convert their star"s sunlight, deficient in some frequencies, to a wavelength which will kill the fungus.'],
'Nitrium': ['Nitrium', 'A metal mined from asteroids, and used in dilithium chambers.'],
'Nocxium': ['Nocxium', 'A highly volatile mineral only formed during supernovas, thus severely limiting the extent of its distribution. Vital ingredient in capsule production, making it very coveted.'],
'Nuridium': ['Nuridium', 'Unstable material used to generate energy, feature in Season 5.'],
'Nvidium': ['Nvidium', 'A rare, superconducting element which is used in production of jump gates. Considered precious by all races, nvidium is especially valuable to Kha"ak who build their homes in nvidium-rich asteroids.'],
'Octiron and Octogen': ['Octiron and Octogen', 'A dense black metal and a magical gas that is a large part of the Discworld"s crust and makes up the atmosphere. It is highly magical with a melting point above the range of metal forges. The gates of Unseen University are made out of it. A needle made of octiron will always point to the Hub, the centre of the Discworld"s magical field; it will also darn its owner"s socks by itself. The University tower bell ("Old Tom") is made of it, and rings audible silences. Coin"s staff in Sourcery was made out of it. In its natural state it releases considerable quantities of magical radiation, but if it becomes negatively polarized, it can be used to absorb such radiation. Octiron under pressure generates significant amounts of heat, which accounts for most of the volcanic geological processes on Discworld (At least, that"s what UU thinks on the matter).'],
'Omega': ['Omega', 'An unstable and vastly dangerous molecule capable of destructive explosions that also disrupt subspace, making warp travel impossible. This atom is a perfect energy source, but also highly unstable and can destroy subspace. Seven of Nine mentions that the Borg revere it religiously due to its perfection and multiple components working together perfectly. By contrast, the United Federation of Planets will ignore all other considerations, including the Prime Directive, to ensure the destruction of the particle if it is detected. Star Trek: Voyager Season 4 (4.21) Episode #89 The Omega Directive, Star Date 51781.2 (Org. Air Date: 15 April 1998)'],
'Onnesium': ['Onnesium', 'Rare element, atomic number 118, mildly radioactive and dangerous, which has been proved to be a viable room-temperature superconductor. Onnesium is normally found as small, silvery spheres embedded within meteoric nickel-iron.'],
'Orichalcum': ['Orichalcum', 'A reddish metal mined in Atlantis, used to make structures and walls. May be based on an actual mineral or gold/copper alloy, possibly Auricupride. Used to power the machinery in Atlantis in the Indiana Jones adventure game. In the Exalted setting Orichalcum is the strongest of the five magical materials and can be made by distilling mundane gold using Gaia"s blood (Magma) and concentrating sunlight using large occult mirrors. It appears in several video games, usually as a material better than "ordinary" mithril. Also named "Orichalcon" in some games, Orichalcum also appears as an alloy in several fictional settings; see below.'],
'Oxyale': ['Oxyale', 'A strange liquid that produces oxygen. Used to breathe underwater.'],
'Padillium': ['Padillium', 'Named for aspiring chemist J. Padilla, Padillium is also known as the "lazy element," in reference to Mr. Padilla"s habit of falling asleep during experiments.[citation needed] It appears on some periodic tables as the very heavy, very inert "Zz."'],
'Phazon': ['Phazon', 'A blue or occasionally orange mutagenic and (in high quantities) toxic substance which is actually a form of inorganic life. Originates from the planet Phaaze, which sends out seeds called "Leviathans" to corrupt planets with it.'],
'Philosopher\'s stone': ['Philosopher\'s stone', 'An mystical element sought by alchemists. It is said to transform any metal in gold and produce the Elixir of Life. In nowdays, it is used in films and cartoons, and shown as a reddish stone.'],
'Philote': ['Philote', 'An infinitely long "string" used biologically and mechanically for instantaneous communication.'],
'Phlogiston': ['Phlogiston', 'A highly flammable medium, similar to the real-world interstellar medium, in which crystal spheres containing whole planetary systems are suspended; travel is conducted by "spelljammer ships", vessels more akin to old sailing ships than science fiction starships. Named after the Phlogiston theory, an obsolete scientific theory of combustion.'],
'Phostlite': ['Phostlite', 'Discovered by Professor Decimus Phostle. Exposure to this element causes living things to grow rapidly to enormous size.'],
'Photonium': ['Photonium', 'Used in starship hull construction. This "photon matter" has almost no mass, allowing for the impressive maneuverability. It can alter its refraction index to absorb light and energy, which is why energy-based weapons and sensors have little to no effect. This matter, however, can only absorb a specific amount of light and energy before becoming overloaded, and thus returning to its original state.'],
'Plutonite': ['Plutonite', 'Oakley uses this name for the polycarbonate lenses in their sunglasses.'],
'Primium': ['Primium', 'A material designed by the Technocracy to resist magical abilities. It is also tough enough to be used as armor plate.'],
'Promethium': ['Promethium', 'An adhesive liquid that acts like napalm on steroids. It can also be used as fuel. Promethium is also a real element.'],
'Protonite': ['Protonite', 'A mineral found only on the planet Proton, it was used throughout the galaxy as a powerful energy source. On Proton"s magical alternate world, Phaze, it was Phazite, the source of magic energy.'],
'Psitanium': ['Psitanium', 'A element that bestows or amplifies psychic powers... or conversely, drives people insane (or makes them more insane. Delivered to Earth on a meteorite; Indians used them as arrowheads. In Whispering Rock Psychic Summer Camp, they"re also used as currency.'],
'Pyerite': ['Pyerite', 'A soft crystal-like mineral with a very distinguishing orange glow as if on fire. used as conduit and in the bio-chemical industry. Commonly found in many asteroid-ore types.'],
'Pyreal': ['Pyreal', 'Fictional metal found on the planet Auberean and used as currency and to forge weapons.'],
'Quassium B': ['Quassium B', 'Fictional element which featured in a number of books by John Pudney. The title of the books contained the word "Adventure" - eg Monday Adventure, Spring Adventure. The books featured "Fred and I" as main characters.'],
'Radical Isotope': ['Radical Isotope', 'Radical isotopes are one of ten elements with negative atomic weights. They are used by the Spirit of the Abyss to control beings. Detecting radical isotopes reveals a being in league with The Abyss.'],
'Randomonium': ['Randomonium', 'A fluorescent green element, a viscous liquid at room temperature which enables costumes to become the creatures they represent.'],
'Rearden Metal': ['Rearden Metal', 'In Ayn Rand"s Atlas Shrugged, Rearden metal is a fictitious metal alloy invented by Hank Rearden. It is lighter than traditional steel but stronger, and is to steel what steel was to iron. It is described as greenish-blue. Among its ingredients are iron and copper, two metals seldom found together in real-world alloys.'],
'Red mercury': ['Red mercury', 'A substance which it is said to be used in nuclear devices production. It is speculated to be a mercury-derivated or a similar substance, but its exitance wasn"t still proven and remains a mystery.'],
'Red Stone': ['Red Stone', 'A reddish stone made with the Red Water, a high-toxic liquid. It is used as an alchemic amplifier, as it amplifies the transmutation power of alchemists. It is also known as the imcomplete Philosofer"s Stone, because it has similar properties.'],
'Relux': ['Relux', 'Material created from light; indestructible and totally reflective. Used in the hull of the heroes" spaceships, among other things. See also Lux.'],
'Runite': ['Runite', 'A light blue metal that is stronger than mithril or adamantine. It is the most common armor in the game and can be crafted with a smithing level of 85 and over.'],
'Sakuradite': ['Sakuradite', 'An element, plentiful in Japan but rare elsewhere, that possesses incredible superconductive properties. It is used to generate and channel energy in great quantities, and is an essential component of Knightmare Frames" propulsion systems.'],
'Schwartz, liquid': ['Schwartz, liquid', 'A potent spaceship fuel, a small amount of which can propel a space Winnebago incredible distances.'],
'Scrith': ['Scrith', 'A semi-translucent, impossibly strong material that is somewhat ductile under massive force that is used as the foundation of which the Ringworld was constructed. It is described as having a strength similar to the force which binds atomic nuclei. It also has the ability to hold strong magnetic fields, meaning it is a para-magnetic substance. Compare Neutronium.'],
'Shazamium': ['Shazamium', 'Invented by Captain Marvel"s nemesis, Sivana. Its atomic number is 98 (which has since been discovered and named Californium)'],
'Sinisite': ['Sinisite', 'A high-energy material occurring naturally in crystalline form, it is found in white (1983 original game) or blue and green (1999"s Sinistar: Unleashed) variants, usually mined from asteroids. It is used in the building of pieces of technology, or purified to form the high-explosive weapons known as Sinibombs.'],
'Sivanium': ['Sivanium', 'Invented by Captain Marvel"s nemesis, Sivana. Its atomic number is 97 (which has since been discovered and named Berkelium)'],
'Smitherene': ['Smitherene', 'A fictional high explosive used by characters in fiction written by Michael Z. Williamson in his Freehold/Grainne universe. A play on the phrase "Blown to smithereens."'],
'Solenite': ['Solenite', 'A fictional substance in the original version of the science fiction series Battlestar Galactica. It may or may not be derived from solium.'],
'Solium': ['Solium', 'A fictional substance in the original version of the science fiction series Battlestar Galactica. It may or may not be used in explosives.'],
'Solium': ['Solium', 'A highly radioactive element utilized by the Terran Federation in a neutron bomb-type doomsday weapon to hold down hostile planets without a large military garrison.'],
'Soulsteel': ['Soulsteel', 'The newest and the second strongest of the five magical materials, formed by alloying human souls and ore dredged up from the nightmares of dead elder gods that teeter upon the edge of oblivion. They always bring with them the chill of the abyss.'],
'Starmetal': ['Starmetal', 'The rarest of the five magical materials, created by the remaining essence of fallen gods.'],
'Strongium 90': ['Strongium 90', 'Used by gym owner Wally Airhead and his men in the episode Leonardo Cuts Loose. Provides the user with strength.'],
'Stupidium': ['Stupidium', 'Used in several circumstances, many times to make fun of scientific jargon, especially of the use of names of elements with the suffix "-ium".'],
'Stygium': ['Stygium', 'Dull black metal which heats up in the presence of light; direct sunlight will cause it to burn or explode. Typically made into rings which are always worn under a glove, usually by alumni of the Assassins Guild because of the colour. Havelock Vetinari, an Assassins Guild alumus, wears a Stygium ring with the initial "V" carved into it. In Making Money A copy of Vetinari"s Stygium ring was worn by Cosmo Lavish and caused Cosmo"s finger to turn gangrenous as it was too tight for his fingers. The finger was removed by Moist Von Lipwig in an emergency amputation by placing the hand (and therefore the ring) in direct sunlight.'],
'Supermanium': ['Supermanium', '"The strongest metal known to science!...forged by him (Superman) from the heart of a mighty star!" A metallic ore designed to mimic Superman’s powers, as well as absorb red-sun light and Kryptonite radiation. Apparently doesn"t exist post-Crisis on Infinite Earths.'],
'Thaesium': ['Thaesium', 'Radioactive element used as fuel for spaceships of the Earth Empire during the 30th century that also serves an important role in the lifecycle of the native inhabitants of the planet Solos.'],
'Thiotimoline': ['Thiotimoline', 'Chemical compound conceived by science fiction author Isaac Asimov and first described in a spoof scientific paper titled "The Endochronic Properties of Resublimated Thiotimoline" in 1948. Thiotimoline is notable for the fact that when it is mixed with water, the chemical actually begins to break down before it contacts the water'],
'Thorium': ['Thorium', 'Metal found on Azeroth that has a silvery green tint and is said to be as strong as steel but as heavy as lead. Used to construct heavier weapons and armour. Should not be confused with the real life Thorium.'],
'Thyrium': ['Thyrium', 'A non-terrestrial element, and supposed not even indigenous to Earth"s solar system, a rare element only observed in trace elements in meteorite crater walls. It is evidently stable, trans-uranic, non-radioactive and apparently fissionable - producing several orders of magnitude more energy than either Uranium or Plutonium without generating waste products or measurable radiation.'],
'Tibanna': ['Tibanna', 'A metallic gas mined from certain gas giants (notably Bespin), it has many high-tech applications including use as high quality hyperdrive coolant and to increase the effectiveness of blaster weapons.'],
'Tiberium': ['Tiberium', 'Tiberium is a fictional crystal found in the game Command and Conquer. Typically green, it is named after the place of its initial discovery on the Tiber River in Italy in the late 20th Century, Although the Brotherhood Of Nod claims it is named after Emperor Tiberous. It leaches metals out of the soil, concentrating them in crystals which can easily be collected and processed. It also converts other matter into more tiberium. The leaching process leaves the landscape depleted, leaving the ground underneath effectively useless for agriculture. Human exposure to this element can trigger mutations, but it more often proves fatal.'],
'Timonium': ['Timonium', 'Timonium is a fictional resource from the Microsoft game, Rise of Legends. It is initially mined from the ground as an ore, and is used both to construct new technology and provide energy.'],
'Tiny Atoms': ['Tiny Atoms', 'Presumably essentailly the same as regular atoms, except much smaller. They are vital to the process of shrinking, but are very expensive, making the construction of remote-controlled "microdroids" a more economical option.'],
'Transparent aluminum': ['Transparent aluminum', 'Strong, lightweight, transparent material used for making windows and other transparent partitions.'],
'Trilithium': ['Trilithium', 'An experimental compound capable of stopping all fusion within a star. Dr. Soran used this in an attempt to return to the spatial anomaly known as the Nexus (Star Trek Generations).'],
'Trilithium Resin': ['Trilithium Resin', 'A hazardous by-product generated by the matter-antimatter reactions in warp cores, it is considered to have no practical use other than as an explosive. Mentioned in the episode Starship Mine.'],
'Trinium': ['Trinium', 'Alien material used in the show as a substance 100 times stronger than steel, which makes up the Stargate"s Iris.'],
'Tritanium': ['Tritanium', 'The main building block in space structures. A very hard, yet bendable metal. Cannot be used in human habitats due to its instability at atmospheric temperatures. Very common throughout the universe.'],
'Tronium': ['Tronium', 'An alien mineral several times more radioactive than Uranium, it is used as a power source for the RTX-011 Hückebein Mk III, R-2 Powered, R-GUN Powered, and SRX. It is also the ammunition used in the battleship Hagane"s Tronium Buster Cannon. Only six chunks of this material are said to exist on Earth.'],
'Turbidium': ['Turbidium', 'In the movie Total Recall, it was a metal\alloy mined for use as a war material on Earth and ultimately used to extract oxygen from the ice in Mars"s core.'],
'Turbonium': ['Turbonium', 'The focal point of the first commercial for the turbo-charged version of the New Beetle. In theory, it was the element from which the turbo version of the car was forged. Also, heroes in the comic Dork Tower fear the dreaded Turbonium Dragon'],
'Tylium': ['Tylium', 'A fictional ore in both versions of the science fiction series Battlestar Galactica. It is very rare throughout the known universe, but essential for fueling both human and Cylon space ships, including for the purpose of faster-than-light jumps. Also referred to as "Tylinium."'],
'Unobtainium': ['Unobtainium', 'Unobtainium is really any material that is unobtainable (for example, titanium was called "unobtainium" during the "60s within American aerospace due to the Soviets" cornering the market); although it can be that it possesses properties that are unlikely or impossible for any real material to possess and is hence completely unobtainable. It is also an informal name for an improbably strong material found in works of science fiction, only used explicitly in The Core. It is typically used to fill a plot hole, allowing characters to do things that may not be physically possible even in principle; thus a possibly more correct term is "handwavium." The form in the movie The Core was technically not an element. It was a Tungsten-Titanium matrix.'],
'Upsidaisium': ['Upsidaisium', 'Upsidaisium is a metal that is lighter than air and can be obtained by mining in upsidaisium-rich areas.'],
'Uridium': ['Uridium', 'Name for the game"s top level, a metallic element the developer thought existed.'],
'Vibranium': ['Vibranium', 'An alien metal that exists in two forms. Wakandan vibranium absorbs vibrational energy (e.g. sound). The more energy it stores the tougher it becomes, due to the energy reinforcing its molecular bonds. If the bonds are broken, all the energy is released, causing an explosion. It is found only in the African nation of Wakanda, ruled by the Black Panther. The other form, Antarctic vibranium, emits a vibration that separates the bonds of other metals, liquifying them.'],
'Vik-ro': ['Vik-ro', 'One of the two components of Lor (see below), which when combined with Yor-san results in total annihilation of the Lor, releasing tremendous energy.'],
'Vionesium': ['Vionesium', 'In the serial Terror of the Vervoids, Vionesium is described as a rare metal from the planet Mogar. It burns brightly in air, similarly to Magnesium. The Sixth Doctor used this effect to destroy the plant based Vervoids by accelerating them through their lifecycle.'],
'Vizorium': ['Vizorium', 'A rare metal used in the construction of warp engines in the Dirty Pair universe. First referenced in the Dirty Pair movie, Project EDEN.'],
'Volucite': ['Volucite', 'Levitation Stone in romaji, is speculated to be its English version "Volucite".'],
'Warpstone or Wyrdstone': ['Warpstone or Wyrdstone', 'A greenish-black crystal apparently of solidified magic that holds tremendous transmutatory powers: Among other things, it can be used as fuel, or even to turn base metal into gold. Its chaotic nature makes it difficult to use, and more often than not causes mutations and unstable weaponry in those dealing with it.'],
'Wellstone': ['Wellstone', 'Formally known as Quantum Wellstone, it is a quantum dot, programmable substrate that can emulate the properties of other elements, including the copyrighted atom Bunkerlite, impervium, and various other super-reflectors and super-absorbers.'],
'Wishalloy': ['Wishalloy', 'An alternative to unobtainium. Historically Scramjets have been described as being made from unobtainium reinforced wishalloy'],
'Wonderflonium': ['Wonderflonium', 'A material used by Dr. Horrible to create a ray that freezes its victim in time. Its container warns against bouncing it. Other properties remain unknown.'],
'Xenothium': ['Xenothium', 'Mysterious substance, presumably liquid or gas, used by Professor Chang to power Red X"s costume and weapons.'],
'Xentronium': ['Xentronium', 'Fictional substance used as an armor on alien ships. Whether it is an element or alloy is unclear.'],
'Yor-san': ['Yor-san', 'One of the two components of Lor (see above) which when combined with Vik-ro results in total annihilation of the Lor, releasing tremendous energy.'],
'Yuanon': ['Yuanon', 'A massive subatomic particle that emits a constant stream of energy (on the order of 500 MW). It is the "closed" form of a planespace Sord (the open form being the 1000 km wide, whitehole-like gateway into planespace).'],
'Zexonite': ['Zexonite', 'An elemental ore not found on Earth, it is taken from a meteorite and used to complete the Phase-Distorter, a machine capable of sending metals and souls, but not complex organic matter, across time.'],
'Zfylud Crystal': ['Zfylud Crystal', 'An elemental alien material found on the planet Balmar. Named after the Balmarian god of creation and divine justice, Zfylud crystals are capable of self-replication and radiate energy that can be harnessed as a power source. The crystals also gain sentience in large numbers and are thus used by the Ze Balmary empire in its giant robots as a power source. Their most advanced mech, also named Zfylud, can change its form to adapt to its enemies. In the Original Generation series, a large chunk of Zfylud crystals assumed sentience and called itself the Septuagint. It appeared as the final boss of the aforementioned game.'],
'Zoridium': ['Zoridium', 'The most powerful explosive substance available in the novel"s timeframe (i.e. before the splitting of the atom). Known to the Sujing Quantou orders as "Daughter of the Sun". Used to power the torpedoes of pirate lord Sheng-Fat and the Coterie of St. Petersburg"s gravity experiments'],
'Zuunium': ['Zuunium', 'A rare element in metallic form, found on the planet Zuun. One of the strange effects of its radiation is that it gives anyone exposed to it the powers of lycanthropy. One such "victim" of exposure became the Legionnaire Timber Wolf.'],
'Zydrine': ['Zydrine', 'Only found in huge geodes; rocks on the outside with crystal-like quarts on the inside. The rarest and most precious of these geodes are those that contain the dark green zydrine within. Very rare and very expensive.'],
}
class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    items = models.CharField(max_length=500, default="DEFAULT ITEM", blank=True, null=True)
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    pos_x = models.PositiveIntegerField()
    pos_y = models.PositiveIntegerField()
    # x = models.PositiveIntegerField()
    # y = models.PositiveIntegerField()


    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()
    def item(self, room):
        ITEM_CREATE_RATE = .55
        self.location = room
        if random.random() > ITEM_CREATE_RATE:
            # new_item = Item.spawn_item(self.location)
            new_item = Item.objects.values_list('name', 'description')
            random_item = random.choice(new_item)
            # print("new item****",new_item) # <Item: Common Kairoseki>.
            # print("random item****",random_item)
            return random_item
            # print('***',Item.spawn_item(self.location))
        else:
            # print("room.item****",Room.item(room))
            return None
    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    inventory = models.CharField(max_length=500, default="No items in inventory")
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            # self.inventory = Player.objects.get(self.inventory)
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()
    def item(self):
        # room_items = Item.objects.filter(roomID = self.id)
        # print("roomitems******",room_items)
        # generates items in rooms, otherwise, there will never be more items in a room once they are deleted
        ITEM_CREATE_RATE = .55
        if random.random() > ITEM_CREATE_RATE:
            spawn = Item.spawn_item()
        else:
            return "Nothing here"
        # print("****************",Item.spawn_item(self.location))

        # print("****************",Item.spawn_item(self.location))
        # else:
        #     return False
    # def checkInventory(self):
    #     # return f'Inventory: Item.objects.get(id=self.inventory)'

    #     return Player.objects.get(id=self.inventory)
    # def pickUpItem(self, item):
    #     itemID = Room.item.id
    #     self.inventory = Item.objects.get(id=Room.itemID)
    #     Room.objects.remove(id=Room.itemID)
    #     self.save()
    # def dropItem(self, item):
    #     itemID = Room.item.id
    #     self.inventory = Item.objects.remove(id=Room.itemID)
    #     Room.objects.add(id=Room.itemID)
    #     self.save()

class Item(models.Model):
    name = models.CharField(max_length=50, default="DEFAULT NAME", blank=True, null=True)
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION", blank=True, null=True)
    # location = models.ForeignKey('adventure.Room', on_delete=models.PROTECT)
    # slot = models.CharField(max_length=10)
    # def pickUpItem(self, item):
    @classmethod
    def spawn_item(cls):
        material = random.choice(list(MATERIAL_NAMES.values()))
        slot = random.choice(['helmet', 'chest', 'waist', 'pants', 'boots', 'weapon'])
        name = f'{random.choice(QUALITY_NAMES)} {material[0]}' #took out SLOT_NAMES
        description = material[1]
        # room = room

        item = Item(name=name, description=description)
        item.save()
        return item
    def __str__(self):
        return self.name
    # def item(self, room):
    #     ITEM_CREATE_RATE = .55
    #     self.location = room
    #     new_item = Item.spawn_item(self.location)
    #     print("new item****",new_item) # <Item: Common Kairoseki>.
    #     return Item.objects.values_list('name', 'description')
@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()