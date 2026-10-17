#!/usr/bin/env python3
"""Author and append the Book 19 (Tigers at Twilight) reading set.

50 items (5 per chapter), same ability-oriented schema as Books 1-16.  Every
``evidence`` string is verified to occur verbatim in the rebuilt chapter text
before writing.  Book 19 is docx-sourced, so its chapter text is reconstructed
here exactly as ``rebuild_docx_book`` builds it (book19_text + rebuild_book19
FIXES + cleanup).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import book19_text as bt
import rebuild_book19 as rb
import rebuild_docx_book as rdb

TARGET = ROOT / 'data' / 'questions.json'

# Balanced, non-repeating answer positions (one five-question row per chapter).
# Totals across the book: A 12, B 13, C 13, D 12.
ANSWER_PATTERNS = ('CABDB', 'DBCAC', 'ACDBD', 'BADCA', 'DCBAB',
                   'ADCBC', 'CDBAD', 'BCADA', 'DACBC', 'BDCAB')

META = {
    'DETAIL': ('RL.5.1', 'Explicit comprehension', 1, '基础'),
    'SEQUENCE': ('RL.5.3', 'Sequence', 2, '进阶'),
    'PLOT RELATION': ('RL.5.3', 'Character/event relationship', 2, '进阶'),
    'VOCABULARY IN CONTEXT': ('RL.5.4', 'Vocabulary in context', 1, '基础'),
    'SUMMARY': ('RL.5.2', 'Summary', 2, '进阶'),
    'INFERENCE': ('RL.5.1', 'Evidence-based inference', 2, '进阶'),
    'CAUSE / PURPOSE / RESULT': ('RL.5.3', 'Cause / purpose / result', 2, '进阶'),
}


def rationale_for(tag, correct):
    if tag == 'VOCABULARY IN CONTEXT':
        return f'结合原句语境，这个词在这里最接近“{correct}”。'
    if tag == 'SEQUENCE':
        return f'按照本章事件先后顺序，最先/最后发生的是：{correct}'
    if tag == 'SUMMARY':
        return f'这个选项同时保留了本章开端与后续的关键事件：{correct}'
    if tag == 'INFERENCE':
        return f'原文细节支持这一推断：{correct}'
    if tag == 'PLOT RELATION':
        return f'结合人物与事件的关系，正确的是：{correct}'
    if tag == 'CAUSE / PURPOSE / RESULT':
        return f'结合事件的原因、目的或结果，正确关系是：{correct}'
    return f'原文直接写到：{correct}'


CH = {
    1: [
        ('DETAIL', 'Which two gifts had Jack and Annie already gotten before this adventure?',
         {'A': 'A pocket watch from the Titanic and an eagle’s feather from the Lakota.',
          'B': 'A seashell from the ocean and a parrot feather from the jungle.',
          'C': 'A gold coin from a pirate ship and a buffalo horn from the plains.',
          'D': 'A silver key from Camelot and a map of the Great Plains.'}, 'A',
         ['a pocket watch from the Titanic and an eagle’s feather from the Lakota Indians of the Great Plains.']),
        ('VOCABULARY IN CONTEXT', 'Morgan’s note says, “This little dog is under a spell.” Here a “spell” is ___.',
         {'A': '魔咒；魔法', 'B': '拼写（单词）', 'C': '一段（天气）时期', 'D': '一场疾病'}, 'A',
         ['This little dog is under a spell and needs your help.']),
        ('CAUSE / PURPOSE / RESULT', 'Why must Jack and Annie collect four special gifts?',
         {'A': 'To free Teddy from the spell he is under.',
          'B': 'To give Morgan presents for her birthday.',
          'C': 'To fill the empty shelves in the tree house.',
          'D': 'To win a contest at the Frog Creek library.'}, 'A',
         ['To free him, you must be given four special things:',
          '“Let’s get going,” said Annie, “so we can free Teddy.”']),
        ('INFERENCE', 'Morgan’s note asks for “a gift from a forest far away.” After Jack reads the title of the research book, what can Jack and Annie figure out?',
         {'A': 'The faraway forest they must visit is in India.',
          'B': 'The forest is the Frog Creek woods near their home.',
          'C': 'They must find a kangaroo in a faraway forest.',
          'D': 'The gift is hidden inside the research book.'}, 'A',
         ['Now we have to get the gift from a forest far away,” said Annie.',
          'Jack picked it up and read the title: Wildlife of India.']),
        ('SEQUENCE', 'Which event happens FIRST in this chapter?',
         {'A': 'Annie spots Teddy peeking out from the bushes.',
          'B': 'Teddy paws a book in the corner of the tree house.',
          'C': 'Annie reads Morgan’s note out loud.',
          'D': 'The tree house starts to spin.'}, 'A',
         ['A small dog with tan-colored fur was peeking out from the bushes.']),
    ],
    2: [
        ('DETAIL', 'According to Jack’s book, what does the word “langur” mean?',
         {'A': 'Having a long tail.', 'B': 'Small gray monkey.',
          'C': 'Swinging from trees.', 'D': 'Friend of the forest.'}, 'A',
         ['This monkey is called a langur', '“having a long tail.”']),
        ('VOCABULARY IN CONTEXT', 'Jack noticed “long, deep gashes in a tree.” A “gash” is ___.',
         {'A': '很深的划痕；裂口', 'B': '鸟窝；树洞', 'C': '一串果实', 'D': '新长出的嫩芽'}, 'A',
         ['Jack noticed long, deep gashes in a tree as they walked by.',
          'They leave big gashes in the bark.']),
        ('INFERENCE', 'Annie says the forest is “like paradise,” but Jack reminds her of the book’s title, Wildlife of India. This shows that Jack ___.',
         {'A': 'is more careful than Annie and worries about hidden dangers',
          'B': 'thinks the forest is boring and wants to go home',
          'C': 'is not interested in any of the forest animals',
          'D': 'believes there are no dangerous animals in India'}, 'A',
         ['“It’s like paradise,” said Annie.',
          '“Yeah, but don’t forget the title of our book: Wildlife of India,” said Jack.']),
        ('CAUSE / PURPOSE / RESULT', 'What does Jack figure out after he reads about the gashes in the tree?',
         {'A': 'Tigers live in this forest, and one has just come this way.',
          'B': 'Elephants have been eating the bark off the trees.',
          'C': 'The langurs scratched the tree while they were playing.',
          'D': 'Someone has been cutting trees to build a house.'}, 'A',
         ['Tigers sharpen their claws on tree trunks. They leave big gashes in the bark.',
          'Tigers live here.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Jack and Annie land at the edge of a forest in India, follow two playful langurs into the trees, and find signs that a tiger is nearby.',
          'B': 'Jack and Annie land beside a stream, ride an elephant through the night, and fall asleep under the full moon.',
          'C': 'Jack and Annie land in a quiet forest, meet a blind hermit, and receive a white lotus flower as a gift.',
          'D': 'Jack and Annie land near a busy village, buy food at a market, and ask the people where the tigers live.'}, 'A',
         ['The tree house was in a tree by a stream at the edge of a forest.',
          'Kah pulled Jack toward the forest.']),
    ],
    3: [
        ('DETAIL', 'According to Jack’s book, how much meat does a wild tiger eat in a year?',
         {'A': 'Almost 5,000 pounds of fresh raw meat.',
          'B': 'About 500 pounds of fish and fruit.',
          'C': 'Almost 50,000 pounds of cooked meat.',
          'D': 'About 50 pounds of small birds.'}, 'A',
         ['A wild tiger eats almost 5,000 pounds of fresh raw meat a year.']),
        ('VOCABULARY IN CONTEXT', '“The snake was slithering around the trunk.” To “slither” means to ___.',
         {'A': '（像蛇一样）扭动着滑行', 'B': '快速地跳来跳去', 'C': '静静地盘着睡觉', 'D': '大声地发出嘶嘶声'}, 'A',
         ['The snake was slithering around the trunk.']),
        ('CAUSE / PURPOSE / RESULT', 'When the monkeys, peacocks, and deer suddenly start crying out, why does Jack put Teddy in his pack?',
         {'A': 'To keep Teddy safe from whatever danger is near.',
          'B': 'Because Teddy is too tired to keep walking.',
          'C': 'So Teddy can sniff out the gift from inside.',
          'D': 'Because the langurs are afraid of little dogs.'}, 'A',
         ['“We better put Teddy in my pack,” said Jack, “to keep him safe.”']),
        ('INFERENCE', 'After reading that the python is not poisonous, Annie says, “Whew.” Why does Jack answer, “Not so fast”?',
         {'A': 'The python can still squeeze its prey to death and swallow a deer-sized animal.',
          'B': 'Jack thinks the python is really a different, poisonous kind of snake.',
          'C': 'Jack knows the python is friendly and only wants to play with them.',
          'D': 'The python is far too slow to ever climb up to their branch.'}, 'A',
         ['To kill its prey, the python squeezes it to death, then swallows it whole.',
          'A python can swallow an animal the size of a full-grown deer.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Kah and Ko swing on vines into another tree.',
          'B': 'Jack and Annie hear a deep, fierce growl.',
          'C': 'Jack reads that the python is not poisonous.',
          'D': 'Jack puts Teddy into his backpack.'}, 'A',
         ['They swung over bushes and tall grass and landed in another tree.']),
    ],
    4: [
        ('DETAIL', 'What did the “thick gray tube” waving in the air turn out to be?',
         {'A': 'An elephant’s trunk.', 'B': 'Another giant python.',
          'C': 'A long, thick jungle vine.', 'D': 'The tiger’s striped tail.'}, 'A',
         ['A thick gray tube was waving in the air.', '“No! An elephant trunk!” said Annie.']),
        ('VOCABULARY IN CONTEXT', 'When the tiger leaped up, “His teeth shone like daggers.” A “dagger” is ___.',
         {'A': '匕首；短剑', 'B': '钻石', 'C': '星星', 'D': '镜子'}, 'A',
         ['His teeth shone like daggers.']),
        ('INFERENCE', 'Jack hears chewing and crunching below and groans, “Now the tiger’s eating the tree.” Why does Annie burst into laughter?',
         {'A': 'She can see the noise is really an elephant eating leaves, not the tiger.',
          'B': 'She thinks the tiger is chewing on Jack’s backpack down below.',
          'C': 'The langurs are tickling her with their long gray tails.',
          'D': 'She knows that tigers love to eat leaves and tree branches.'}, 'A',
         ['From below came loud sounds of chewing, smacking, and crunching.',
          'One stood beneath their tree, eating leaves.']),
        ('CAUSE / PURPOSE / RESULT', 'What happens when the tiger leaps at Jack and Annie as they swing on the vines?',
         {'A': 'His claws barely miss them, and he crashes back down into the bushes.',
          'B': 'He grabs Jack’s backpack and pulls it down to the ground.',
          'C': 'He catches hold of a vine and climbs up after them.',
          'D': 'He knocks Annie off her vine into the tall grass.'}, 'A',
         ['His claws barely missed Jack and Annie!', 'The tiger crashed back down into the bushes.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Jack and Annie swing away from the python, barely escape a leaping tiger, and then discover a herd of elephants below their tree.',
          'B': 'Jack and Annie fight off the python with sticks, chase the tiger away, and climb down to look for the tree house.',
          'C': 'Jack and Annie fall from their vines, hide deep in the bushes, and wait all night for the langurs to return.',
          'D': 'Jack and Annie ride the tiger through the forest, feed the hungry elephants, and find the gift in a tree.'}, 'A',
         ['Like a flame, a tiger leaped up from the bushes!',
          'In the gray gloom, they saw a herd of elephants.']),
    ],
    5: [
        ('CAUSE / PURPOSE / RESULT', 'Why does Annie think riding on an elephant is a good way to travel through the forest?',
         {'A': 'Their book said tigers don’t attack elephants, so they would be safe.',
          'B': 'Elephants can run much faster than any tiger in the forest.',
          'C': 'The elephant knows exactly where the forest gift is hidden.',
          'D': 'Riding an elephant is the only way to cross the deep stream.'}, 'A',
         ['Our book said tigers don’t attack elephants, right?',
          'So we should travel through the forest on the back of an elephant,” said Annie.']),
        ('DETAIL', 'Who leads the way as the elephants march through the forest?',
         {'A': 'Kah and Ko, the two langurs.', 'B': 'Teddy, barking from the front.',
          'C': 'Annie, steering Saba by her ears.', 'D': 'A group of small deer.'}, 'A',
         ['Kah and Ko bounded ahead of them, two moon shadows leading the way.']),
        ('VOCABULARY IN CONTEXT', 'When a long roar split the night, “A chill went down Jack’s spine.” This means Jack ___.',
         {'A': '突然感到害怕，背脊发凉', 'B': '觉得夜里太冷，想穿外套',
          'C': '从大象背上滑下来摔伤了背', 'D': '高兴得浑身发抖'}, 'A',
         ['Suddenly, a long roar split the night.', 'A chill went down Jack’s spine.']),
        ('INFERENCE', 'When Annie says the elephant “just told me” her name is Saba, Jack says, “Yeah, right.” This shows that Jack ___.',
         {'A': 'doesn’t believe an elephant could really tell Annie her name',
          'B': 'thinks Saba is a beautiful name for an elephant',
          'C': 'already knew the elephant’s name from the book',
          'D': 'is upset that Annie climbed onto the elephant first'}, 'A',
         ['“That’s her name,” said Annie. “She just told me.”', '“Yeah, right,” said Jack.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'Jack falls asleep with his head on Saba’s back.',
          'B': 'Annie climbs down onto Saba’s back first.',
          'C': 'Saba rests her trunk on Jack’s head.',
          'D': 'A long roar splits the night and turns into moaning.'}, 'A',
         ['Soon Jack’s head rested on Saba’s back.']),
    ],
    6: [
        ('DETAIL', 'Where is Annie when Jack wakes up on Saba’s back?',
         {'A': 'Sitting barefoot on a big black rock downstream.',
          'B': 'Riding on the back of another elephant.',
          'C': 'Sleeping inside the magic tree house.',
          'D': 'Swinging on vines with Kah and Ko.'}, 'A',
         ['She was sitting on a big black rock downstream. She was barefoot and soaking wet.']),
        ('VOCABULARY IN CONTEXT', 'The book says the Indian rhino is “a very endangered animal. This means that there are not many left.” “Endangered” means ___.',
         {'A': '濒临灭绝的；数量很少的', 'B': '非常危险、会伤人的', 'C': '只生活在水里的', 'D': '视力很差的'}, 'A',
         ['The Indian rhino is a very endangered animal. This means that there are not many left.']),
        ('CAUSE / PURPOSE / RESULT', 'According to Jack’s book, why do rhinos sometimes charge at things by mistake?',
         {'A': 'Because they do not see well.',
          'B': 'Because they are always hungry.',
          'C': 'Because loud noises make them angry.',
          'D': 'Because they are guarding their babies.'}, 'A',
         ['But because they do not see well, they sometimes charge at things by mistake.',
          'Too bad animals can’t wear glasses, he thought.']),
        ('PLOT RELATION', 'How does the information in Jack’s book help Annie when the rhino points his horn at her?',
         {'A': 'Jack knows a loud noise will usually stop a rhino, so Annie claps and shouts and the rhino stops.',
          'B': 'Jack knows rhinos are afraid of dogs, so Annie calls for Teddy and the rhino runs away.',
          'C': 'Jack knows rhinos cannot swim well, so Annie wades into deeper water to escape.',
          'D': 'Jack knows rhinos love flowers, so Annie offers the rhino a white flower to eat.'}, 'A',
         ['“Make a loud noise!” Jack yelled.', 'The rhino stopped. He grunted. Then he sank back into the water.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'Jack wakes up by a misty stream, slides off Saba into the mud, and reads about rhinos just before one rises from the water and almost charges at Annie.',
          'B': 'Jack wakes up in the tree house, finds that Annie is gone, and searches the forest for her until the sun goes down.',
          'C': 'Jack wakes up on Saba’s back, rides her across the wide stream, and catches silver fish for everyone’s breakfast.',
          'D': 'Jack wakes up by a stream, sees a tiger drinking the water, and hides in the mud until the tiger finally leaves.'}, 'A',
         ['“Thanks for the ride,” he said softly.',
          'The rhino rose from the stream. He looked like an ancient swamp creature.']),
    ],
    7: [
        ('DETAIL', 'What was wrong with the tiger that Annie found?',
         {'A': 'His front paw was caught in a trap.',
          'B': 'He had fallen into a deep muddy hole.',
          'C': 'He had been squeezed by the python.',
          'D': 'He was stuck high up in a tree.'}, 'A',
         ['The tiger was lying on his side, completely still.', 'His front paw was caught in a trap.']),
        ('VOCABULARY IN CONTEXT', 'The book says that if the killing does not end, tigers and rhinos “face extinction.” “Extinction” means ___.',
         {'A': '灭绝（世界上再也没有这种动物）', 'B': '被关进动物园', 'C': '搬到别的森林去生活', 'D': '生病或受伤'}, 'A',
         ['Extinction means that someday there may be no Indian tigers or rhinos left on earth.']),
        ('PLOT RELATION', 'Annie says the trapped tiger “must have gotten caught last night. That’s the sad sound we heard.” Which earlier sound is she talking about?',
         {'A': 'The long roar that turned into moaning while they rode the elephants.',
          'B': 'The screeching and cawing of the birds when they first landed.',
          'C': 'The short barking sounds the small deer made in the forest.',
          'D': 'The slurpy, sloshing sound the rhino made in the stream.'}, 'A',
         ['He must have gotten caught last night. That’s the sad sound we heard.']),
        ('CAUSE / PURPOSE / RESULT', 'After reading the book, what makes Jack say, “Oh, man, we do have to save him”?',
         {'A': 'He learns that poachers trap and kill tigers, and that tigers could become extinct.',
          'B': 'He learns that tigers are gentle animals that never attack people.',
          'C': 'He learns that the trap will soon snap shut on Annie’s hand.',
          'D': 'He learns that the tiger is a pet that belongs to the hermit.'}, 'A',
         ['After trapping a tiger, they kill it and sell the body parts for money.',
          'If the killing does not end, they both face extinction.']),
        ('SEQUENCE', 'Which event happens LAST in this chapter?',
         {'A': 'The tiger gets to his feet and snarls at Jack and Annie.',
          'B': 'Jack pushes down the lever and raises the bar.',
          'C': 'Annie strokes the tiger’s fur gently.',
          'D': 'Jack shows Annie the picture of the trap.'}, 'A',
         ['The tiger was on his feet. He stared right at them.', 'The tiger snarled at Jack and Annie.']),
    ],
    8: [
        ('DETAIL', 'When Teddy barks fiercely at Annie, what does she say he is telling them?',
         {'A': 'To run and hide.', 'B': 'To climb a tree.',
          'C': 'To stand still and be quiet.', 'D': 'To fight the tiger together.'}, 'A',
         ['“Teddy says run and hide!” said Annie.']),
        ('VOCABULARY IN CONTEXT', 'After the tiger leaves, “Teddy was just like a small scruffy dog again.” “Scruffy” means ___.',
         {'A': '毛发蓬乱、脏兮兮的', 'B': '凶猛可怕的', 'C': '高大强壮的', 'D': '干净整洁的'}, 'A',
         ['Teddy was just like a small scruffy dog again.']),
        ('INFERENCE', 'Jack hears growls grow “louder and louder” and says, “That doesn’t sound like Teddy.” Later he asks Teddy, “Did you turn into a wild dog?” What do these clues suggest?',
         {'A': 'Teddy may have used some kind of magic to become fierce enough to scare off the tiger.',
          'B': 'A real pack of wild dogs came out of the forest to help Jack and Annie.',
          'C': 'The tiger was growling at the langurs in the trees, not at Teddy.',
          'D': 'Teddy ran away and hid behind the big black rock with Jack and Annie.'}, 'A',
         ['“That doesn’t sound like Teddy,” said Jack.', 'Did you turn into a wild dog?']),
        ('CAUSE / PURPOSE / RESULT', 'Why does Jack say, “I guess we won’t be getting a thank-you gift from that tiger”?',
         {'A': 'The tiger they had just saved came after them instead of thanking them.',
          'B': 'Tigers have no way to carry presents through the forest.',
          'C': 'Teddy had already gotten the gift from the tiger.',
          'D': 'The langurs told Jack the gift was hidden somewhere else.'}, 'A',
         ['The huge tiger limped closer and closer to Jack and Annie.',
          '“Well, I guess we won’t be getting a thank-you gift from that tiger,” he said.']),
        ('SUMMARY', 'Which choice best summarizes this chapter?',
         {'A': 'The freed tiger comes after Jack and Annie, Teddy bravely drives him away, and the langurs lead the children downstream to a peaceful old man.',
          'B': 'The freed tiger becomes friends with Jack and Annie, licks their hands, and then gives them a thank-you gift from the forest.',
          'C': 'Jack and Annie run from the tiger all the way back to the tree house, and then they wish themselves home to Frog Creek.',
          'D': 'Teddy chases the rhino out of the stream, the elephants come back for the children, and Saba carries them to the tree house.'}, 'A',
         ['Teddy stood tall and brave in the grass.',
          'When they went around the bend, they saw a man sitting cross-legged on a rock.']),
    ],
    9: [
        ('VOCABULARY IN CONTEXT', 'The blind man says, “Hermits live far away from other people.” A “hermit” is ___.',
         {'A': '隐士（独自远离人群生活的人）', 'B': '看守森林的人', 'C': '偷猎者', 'D': '驯兽师'}, 'A',
         ['“Hermits live far away from other people,” said the blind man.']),
        ('DETAIL', 'How does the hermit say he learns from nature?',
         {'A': 'He listens to the sounds of the forest animals.',
          'B': 'He reads many books about the forest animals.',
          'C': 'He walks through the forest every single night.',
          'D': 'He asks the langurs to teach him their language.'}, 'A',
         ['“I listen,” said the blind man.',
          'To the chatter of the monkeys, the rumble of the elephant, the roar of the tiger,” said the man.']),
        ('INFERENCE', 'The hermit says the lotus blossom’s “beauty cannot live without its ugliness.” What is he teaching Jack and Annie about the tiger?',
         {'A': 'Saving the tiger means accepting both his beauty and his fierce, wild nature.',
          'B': 'The tiger is too ugly and dangerous, so he should not have been saved.',
          'C': 'A lotus flower can keep people safe from the wild tigers of the forest.',
          'D': 'Beautiful things should always be kept far away from dark, thick mud.'}, 'A',
         ['This perfect lotus blossom grows from dark, thick mud,” he said. “Its beauty cannot live without its ugliness.',
          '“When you saved the tiger, you saved all of him,” said the blind man.']),
        ('CAUSE / PURPOSE / RESULT', 'Why is the tree house close by, even though Jack thought they had traveled far away?',
         {'A': 'The elephants walked in a large circle, so they are back where they started.',
          'B': 'The tree house magically followed them through the forest all night.',
          'C': 'The hermit carried the tree house to a tree beside his cave.',
          'D': 'The langurs led them back by a shortcut across the stream.'}, 'A',
         ['The elephants walked in a large circle. So you are back at the place where you started.']),
        ('PLOT RELATION', 'How is the lotus blossom connected to Morgan’s note?',
         {'A': 'It is the “gift from a forest far away,” given to thank them for saving the tiger.',
          'B': 'It is the “gift from a kangaroo,” which the hermit brought from a faraway land.',
          'C': 'It is the “gift from a ship lost at sea,” which washed up in the stream.',
          'D': 'It is a present for Morgan’s garden, which the langurs picked just for her.'}, 'A',
         ['Take this lotus as a thank-you gift from all the forest for saving our fierce friend,',
          '“A gift from a forest far away,” she said.']),
    ],
    10: [
        ('DETAIL', 'How does Annie say she knew that Teddy wanted them to hide behind the rock?',
         {'A': 'She just knew—she thinks she saw it in his eyes.',
          'B': 'Teddy pointed at the big rock with his paw.',
          'C': 'The hermit told her about it afterward.',
          'D': 'She read about it in the India book.'}, 'A',
         ['“I just knew,” she said. “I think I saw it in his eyes.”']),
        ('VOCABULARY IN CONTEXT', '“The Frog Creek woods were very tame after the forest in India.” Here “tame” means ___.',
         {'A': '平静的；不危险的', 'B': '危险的；野性的', 'C': '茂密的；昏暗的', 'D': '吵闹的；喧哗的'}, 'A',
         ['The Frog Creek woods were very tame after the forest in India.']),
        ('INFERENCE', 'Teddy’s eyes “twinkled, as if they held many secrets,” and Jack whispers, “Who are you, really?” This suggests that Jack ___.',
         {'A': 'suspects that Teddy is much more than an ordinary little dog',
          'B': 'thinks that Teddy is sick and needs to see a doctor',
          'C': 'has suddenly forgotten the little dog’s name',
          'D': 'believes that Teddy really belongs to the hermit'}, 'A',
         ['Teddy’s eyes twinkled, as if they held many secrets.', '“Who are you, really?” whispered Jack.']),
        ('PLOT RELATION', 'Why does Annie tell Teddy, “One more gift, and you’ll be free from your spell”?',
         {'A': 'They now have three of the four special gifts that Morgan’s note asked for.',
          'B': 'Morgan told them that only one more trip to India was needed.',
          'C': 'The hermit promised to send them the very last gift himself.',
          'D': 'Teddy already broke most of the spell by fighting the tiger.'}, 'A',
         ['“One more gift,” she said to Teddy, “and you’ll be free from your spell.”']),
        ('SUMMARY', 'Which choice best summarizes the whole book?',
         {'A': 'Jack and Annie travel to a forest in India, escape a python and a tiger with help from langurs and elephants, free a trapped tiger, and receive a lotus as the third gift to help free Teddy.',
          'B': 'Jack and Annie travel to the Great Plains, live with the Lakota Indians, hunt buffalo on the open prairie, and receive an eagle’s feather as the second gift to help free Teddy.',
          'C': 'Jack and Annie travel on the Titanic, help two children escape the sinking ship, ride in a lifeboat all night, and bring home a pocket watch as the first gift to help free Teddy.',
          'D': 'Jack and Annie travel to Australia, rescue a baby kangaroo from a raging fire, and bring home a gift from the kangaroo as the fourth and final gift to free Teddy.'}, 'A',
         ['“Our third gift,” said Annie.',
          'She put the lotus blossom beside the pocket watch from the Titanic and the eagle’s feather from the Lakota Indians.']),
    ],
}

BOOK_TITLE = 'Tigers at Twilight'
BOOK_TITLE_CN = '丛林猛虎'
CHAPTER_TITLES = ['How Far Away?', 'Kah and Ko', 'Life or Death', 'Swing Time', 'Night Walk',
                  'Swamp Creature', 'Trapped!', 'Wonder Dog', 'The Hermit', 'Who Are You, Really?']


def chapter_text(chapter_index):
    """Rebuild Book 19 chapter text exactly as rebuild_docx_book does."""
    text = bt.chapter_text(chapter_index)
    for old, new in rb.FIXES.get(chapter_index, []):
        if old in text:
            text = text.replace(old, new)
    return rdb._cleanup(text).strip()


def build_book():
    texts = {c: chapter_text(c - 1) for c in range(1, 11)}
    chapters, problems = [], []
    for chapter_number in range(1, 11):
        norm_text = re.sub(r'[“”"\']', '', texts[chapter_number])
        questions = []
        for question_number, (tag, stem, options, answer, evidence) in enumerate(CH[chapter_number], start=1):
            standard, skill, dok, difficulty = META[tag]
            for piece in evidence:
                if re.sub(r'[“”"\']', '', piece) not in norm_text:
                    problems.append(f'ch{chapter_number} Q{question_number}: evidence not found: {piece!r}')
            # Source declarations keep the correct choice first for easy review.
            # Rotate it deterministically in the emitted quiz so learners cannot
            # infer the answer position; distribute A/B/C/D evenly across Book 19.
            labels = 'ABCD'
            correct_text = options[answer]
            distractors = [options[label] for label in labels if label != answer]
            emitted_answer = ANSWER_PATTERNS[chapter_number - 1][question_number - 1]
            emitted_options, distractor_index = {}, 0
            for label in labels:
                if label == emitted_answer:
                    emitted_options[label] = correct_text
                else:
                    emitted_options[label] = distractors[distractor_index]
                    distractor_index += 1
            questions.append({
                'number': question_number, 'standard': standard, 'skill': skill, 'dok': dok,
                'stem': stem, 'options': emitted_options, 'answer': emitted_answer, 'evidence': evidence,
                'rationale': rationale_for(tag, correct_text),
                'id': f'B19C{chapter_number}Q{question_number}', 'difficulty': difficulty,
            })
        chapters.append({'book': 19, 'chapter': chapter_number,
                         'chapter_title': CHAPTER_TITLES[chapter_number - 1], 'questions': questions})
    if problems:
        raise SystemExit('Evidence check failed:\n' + '\n'.join(problems))
    return {'book': 19, 'book_title': BOOK_TITLE, 'book_title_cn': BOOK_TITLE_CN, 'chapters': chapters}


def main():
    data = json.loads(TARGET.read_text(encoding='utf-8'))
    book = build_book()
    data['books'] = [item for item in data['books'] if item.get('book') != 19] + [book]
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('questions.json: Book 19 appended, 10 chapters / 50 questions')


if __name__ == '__main__':
    main()
