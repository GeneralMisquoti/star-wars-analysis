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