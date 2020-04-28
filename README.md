# star-wars-analysis

The _Los Angeles Times_ counted the words spoken by male and female characters in the first eight episodes of the "Star Wars" film series ahead of the release of "Star Wars: The Rise of Skywalker." The analysis found despite the fact that the latest series of films contains greater gender diversity, [male characters still have the most dialogue](https://www.latimes.com/projects/star-wars-movies-female-character-analysis/). The data also allowed us to rank the series' [most talkative characters](https://www.latimes.com/projects/star-wars-most-talkative-characters/). More details on the project are described in [this Q&A](https://www.latimes.com/entertainment-arts/story/2019-12-19/star-wars-movies-female-character-analysis-q-a).

### Methodology

The Times analyzed the movie scripts of the eight entries (so far) in the “Star Wars” saga. The analysis included all English dialogue (Galactic Basic in the films’ universe) that appears in subtitles of the films streaming on Disney+ and Netflix, as well as any fictional languages translated into English.

To count Chewbacca’s words, The Times performed a rough translation of the Wookiee language of Shyriiwook, counting individual growls, moans and roars as one word each. Similarly, R2-D2 and BB-8's individual whistles, beeps, boops and blurts were counted as a single word each, with help from a computer program. Other speakers of alien and droid languages, including Teedospeak, Jawaese and Ewokese, could not be reliably translated without a protocol droid. Lines delivered in such languages were logged instead as one word to establish a minimum presence for the character.

The analysis of dialogue by gender was limited to the first 15 characters listed in the credits of each movie. Humanoid characters that appeared in the credits but spoke no lines in the movie were included in the gender comparison. These characters include Gov. Tarkin and Queen of Naboo in “Revenge of the Sith” and Lando’s Assistant in “The Empire Strikes Back.” Characters that did not speak English or have English subtitles were not included. These characters include Chewbacca, R2-D2, Chief Jawa, Chief Ugnaught and Snow Creature. Characters represented by more than one actor in the film credits were combined for the purpose of this analysis.

Words heard in characters’ dreams or flashbacks did not count, although dialogue delivered via recorded message or conveyed by Force ghost did.

Anakin Skywalker and Darth Vader’s dialogue was counted separately for the sake of documenting the conflicted character’s relationship with others. According to the series’ timeline and for the purposes of the Times analysis, Anakin became Darth Vader when Emperor Palpatine says, “Henceforth, you shall be known as Darth Vader.” The character became Anakin Skywalker again after he threw his master down a shaft on the second Death Star.

Characters in disguise or impersonating another character were counted as the actual speaker. By this rule, Darth Sidious and Palpatine were considered the same character in the prequels, as were Princess Leia Organa and Boushh, the bounty hunter she disguised herself as, in “The Return of the Jedi.” In several scenes of the “The Phantom Menace,” a handmaiden called Sabé acts as a decoy for Queen Padmé Amidala. Using visual cues on-screen— and from other sources, lines delivered by Sabé were counted separately from those said by Padmé.

### Python utilities

Use the `swa.py` file with Python 3.7+ to view basic statistics about the data.

**Get amount of words spoken by `ANAKIN` in each movie:**
```bash
$ python3 swa.py wc anakin
Character {'ANAKIN'} has 1046 words in file 01_phantom_menace.csv
Character {'ANAKIN'} has 1525 words in file 02_attack_of_the_clones.csv
Character {'ANAKIN'} has 1330 words in file 03_revenge_of_the_sith.csv
Character anakin has 0 words in file 04_a_new_hope.csv
Character anakin has 0 words in file 05_empire_strikes_back.csv
Character {'ANAKIN'} has 48 words in file 06_return_of_the_jedi.csv
Character anakin has 0 words in file 07_the_force_awakens.csv
Character anakin has 0 words in file 08_the_last_jedi.csv
```

**See combinations of characters speaking to each other (by movie):**
```bash
$ python3 swa.py wcm anakin obi-wan --group-per-movie
wc matrix: [anakin ✖ obi-wan]
01_phantom_menace.csv;anakin;anakin;6
01_phantom_menace.csv;anakin;obi-wan;17
01_phantom_menace.csv;obi-wan;anakin;16
02_attack_of_the_clones.csv;obi-wan;anakin;640
02_attack_of_the_clones.csv;obi-wan;obi-wan;32
02_attack_of_the_clones.csv;anakin;obi-wan;395
02_attack_of_the_clones.csv;anakin;anakin;28
03_revenge_of_the_sith.csv;anakin;obi-wan;498
03_revenge_of_the_sith.csv;anakin;anakin;4
03_revenge_of_the_sith.csv;obi-wan;anakin;680
03_revenge_of_the_sith.csv;obi-wan;obi-wan;12
04_a_new_hope.csv;obi-wan;obi-wan;11
```

**Convert to a format of your choosing**  

    Format: `(` part number of movie `, ` first column `, ` second column `, ` fourth column 
    `-f 1 2 3` - only first, second and third movie parts  
    `-gpm` - alias of `--group-per-movie`  
    `-c ANAKIN QUI-GON` - only show these characters speaking to each other  
    `-c ANAKIN=1 QUI-GON=3` - the above, and additionaly rename this characters to the given text following `=`  
```bash
$ python3 swa.py cvrt "($partId, $1, $2, '$4')" -f 1 2 3 --gpm -c ANAKIN=1 QUI-GON=3

```

<details>
<summary>
View whole output
</summary>
```
Format: "($partId, $1, $2, '$4')"; files: ['01_phantom_menace.csv', '02_attack_o
f_the_clones.csv', '03_revenge_of_the_sith.csv']
01_phantom_menace.csv:
(1, 1, 3, 'Hi.')
(1, 3, 1, 'Hi there.')
(1, 1, 3, 'Your buddy here was about to be turned into orange goo. He picked a f
ight with a Dug... an especially dangerous Dug called Sebulba.')
(1, 3, 1, 'Thanks, my young friend.')
(1, 1, 3, 'Here, you'll like these pallies. Here.')
(1, 3, 1, 'Thank you.')
(1, 1, 3, 'Do you have shelter?')
(1, 3, 1, 'We'll head back to our ship.')
(1, 1, 3, 'Is it far?')
(1, 3, 1, 'It's on the outskirts.')
(1, 1, 3, 'You'll never reach the outskirts in time. Sandstorms are very, very d
angerous. Come on. I'll take you to my place.')
(1, 1, 1, 'Whoops.')
(1, 1, 3, 'I've been working on a scanner to try and locate mine.')
(1, 1, 3, 'And they blow you up! Boom!')
(1, 1, 3, 'Has anybody ever seen a Podrace?')
(1, 3, 1, 'They have Podracing on Malastare. Very fast, very dangerous.')
(1, 1, 3, 'I'm the only human who can do it.')
(1, 3, 1, 'You must have Jedi reflexes if you race pods.')
(1, 1, 3, 'You're a Jedi knight, aren't you?')
(1, 3, 1, 'What makes you think that?')
(1, 1, 3, 'I saw your laser sword. Only Jedis carry that kind of weapon.')
(1, 3, 1, 'Perhaps I killed a Jedi and took it from him.')
(1, 1, 3, 'I don't think so. No one can kill a Jedi.')
(1, 3, 1, 'I wish that were so.')
(1, 1, 3, 'I had a dream I was a Jedi. I came back here and freed all the slaves
.')
(1, 1, 3, 'Have you come to free us?')
(1, 3, 1, 'No, I'm afraid not.')
(1, 1, 3, 'I think you have. Why else would you be here?')
(1, 3, 1, 'I can see there's no fooling you, Anakin.')
(1, 3, 1, 'We're on our way to Coruscant, the central system in the Republic...
on a very important mission.')
(1, 1, 3, 'How did you end up out here in the outer rim?')
(1, 1, 3, 'I can help. I can fix anything.')
(1, 3, 1, 'I believe you can. But first we must acquire the parts we need.')
(1, 1, 3, 'I built a racer. It's the fastest ever. There's a big race tomorrow o
n Boonta Eve.')
(1, 1, 3, 'You could enter my pod.')
(1, 3, 1, 'Your mother's right.')
(1, 3, 1, 'Is there anyone friendly to the Republic who can help us?')
(1, 1, 3, 'It wasn't my fault. Really. Sebulba flashed me with his vents. I actu
ally saved the pod, mostly.')
(1, 3, 1, 'I think it's time we found out.')
(1, 3, 1, 'Here, use this power charge.')
(1, 1, 3, 'Yes, sir!')
(1, 1, 3, 'It's working! It's working!')
(1, 3, 1, 'Stay still, Ani. Let me clean this cut.')
(1, 1, 3, 'There's so many. Do they all have a system of planets?')
(1, 3, 1, 'Most of them.')
(1, 1, 3, 'Has anyone been to 'em all?')
(1, 3, 1, 'Not likely.')
(1, 1, 3, 'I wanna be the frst one to see 'em all.')
(1, 3, 1, 'There we are. Good as new.')
(1, 1, 3, 'What are you doing?')
(1, 3, 1, 'Checking your blood for infections. Go on. You have a big day tomorro
w. Sleep well, Ani.')
(1, 1, 3, 'What'd he mean by that?')
(1, 3, 1, 'I'll tell you later.')
(1, 3, 1, 'Of course you will.')
(1, 3, 1, 'You all set, Ani?')
(1, 1, 3, 'Yep.')
(1, 3, 1, 'Right. Remember, concentrate on the moment. Feel, don't think. Use yo
ur instincts.')
(1, 1, 3, 'I will.')
(1, 3, 1, 'May the Force be with you.')
(1, 1, 1, 'Oh, no! Nooo!')
(1, 3, 1, 'Hey. These are yours.')
(1, 1, 1, 'Yes!')
(1, 3, 1, 'And he has been freed.')
(1, 1, 3, 'What? ')
(1, 3, 1, 'You're no longer a slave.')
(1, 1, 3, 'You mean I get to come with you in your starship?')
(1, 3, 1, 'Anakin... training to become a Jedi is not an easy challenge... and e
ven if you succeed, it's a hard life.')
(1, 1, 3, 'But I wanna go. It's what I've always dreamed of doing.')
(1, 3, 1, 'Then pack your things. We haven't much time.')
(1, 1, 1, 'Yippee!')
(1, 1, 3, 'What about Mom? Is she free too?')
(1, 3, 1, 'I tried to free your mother, Ani, but Watto wouldn't have it.')
(1, 1, 3, 'Qui-Gon, sir, wait! I'm tired!')
(1, 3, 1, 'Anakin! Drop! Go! Tell them to take off!')
(1, 1, 3, 'Are you all right?')
(1, 3, 1, 'I think so.')
(1, 3, 1, 'I'm not sure... but it was well-trained in the Jedi arts.')
(1, 1, 3, 'What are we gonna do about it?')
(1, 3, 1, 'We shall be patient.')
(1, 3, 1, 'Anakin Skywalker... meet Obi-Wan Kenobi.')
(1, 1, 3, 'Qui-Gon, sir, I don't want to be a problem.')
(1, 3, 1, 'You won't be, Ani. I'm not allowed to train you... so I want you to w
atch me and be mindful. Always remember: Your focus determines your reality. Sta
y close to me and you'll be safe.')
(1, 1, 3, 'Master, sir... I heard Yoda talking about midi-chlorians. I've been w
ondering... What are midi-chlorians?')
(1, 3, 1, 'Midi-chlorians are a microscopic life-form... that resides within all
 living cells.')
(1, 1, 3, 'They live inside me?')
(1, 3, 1, 'Inside your cells, yes. And we are symbionts with them.')
(1, 1, 3, 'Symbionts?')
(1, 3, 1, 'Life-forms living together for mutual advantage. Without the midi-chl
orians, life could not exist... and we would have no knowledge of the Force. The
y continually speak to us... telling us the will of the Force. When you learn to
 quiet your mind... you'll hear them speaking to you.')
(1, 1, 3, 'I don't understand.')
(1, 3, 1, 'With time and training, Ani, you will. You will.')
(1, 1, 3, 'They're here!')
(1, 3, 1, 'Once we get inside, you find a safe place to hide and stay there.')
(1, 1, 3, 'Sure.')
(1, 3, 1, 'Stay there.')
(1, 3, 1, 'Ani, find cover. Quick!')
(1, 1, 3, 'Hey, wait for me!')
(1, 3, 1, 'Anakin, stay where you are. You'll be safe there.')
(1, 1, 3, ' But l...')
(1, 3, 1, 'Stay in that cockpit.')
(1, 3, 1, 'We'll handle this.')


02_attack_of_the_clones.csv:
(2, 1, 1, 'But I am grown up. You said it yourself.')
(2, 1, 1, 'You're exactly the way I remember you in my dreams.')
(2, 1, 1, 'No. No.')
(2, 1, 1, 'Oh, not again. Obi-Wan's gonna kill me.')


03_revenge_of_the_sith.csv:
(3, 1, 1, 'What have I done?')
```
</details>