import re
import math
import random
import time

DAMAGE_TIERS = [
    (90, 100, "💀 SPIRITUALLY EVICTED", "You have officially reached rock bottom. There is no recovery from this.", "Fatal"),
    (80, 89, "🔥 ABSOLUTELY COOKED", "Your ego was placed directly in an industrial furnace.", "Severe"),
    (70, 79, "😭 EMOTIONAL DAMAGE", "This will keep you awake at 3:17 AM for the next six years.", "High"),
    (50, 69, "🤡 SKILL ISSUE & DELUSION", "You thought you did something here, but you're just a clown in denial.", "Moderate"),
    (0, 49, "🤏 MILDLY EMBARRASSING", "Not even worthy of a full roast, just pathetic.", "Mild")
]

# ===========================================================================
# MASSIVE ROAST DATABASE — categorized, high variety, human-feeling
# ===========================================================================

ROAST_DATABASE = {
    "ex": {
        "tag": "REALITY CHECK",
        "roasts": [
            "Two days after they left and you're already drafting a 'hey stranger' message. Let me check the forecast — yep, 100% chance of being left on read.",
            "They literally changed their Netflix password and you're out here acting like that was ambiguous. That's a signed, notarized document saying goodbye.",
            "The fact that you're asking whether to text your ex tells me the answer is obviously no but you're going to do it anyway so why are you even here.",
            "Bro they haven't replied to your last three messages and you're wondering if the timing is right. The timing was never right. That's the timing.",
            "You want to text your ex because it's late and you're lonely. That's not love. That's your body telling you to go drink some water and sleep.",
            "They blocked you on Instagram but not WhatsApp because they enjoy watching the three dots appear and disappear. You're entertainment. Not a priority.",
            "You had six months to fix what was broken. You didn't. Now it's 2 AM and you think a text is going to undo all of that. That's not how any of this works.",
            "The moment they said 'I need space', they were not referring to a slight change in your communication schedule. They meant permanent absence. From you.",
            "They liked your story but didn't reply. That's not a green light. That's someone hitting the wrong button while half asleep.",
            "You two broke up three times already and you want to try again. The fourth time is not the charm. The fourth time is just evidence.",
            "I love how you're calling it 'checking in'. You're not checking in. You're chasing dopamine at 1 AM while they're genuinely fine.",
            "They're posting happy Instagram content. You're here asking me if you should text them. One of you has moved on. It's not you.",
            "Stop romanticizing what you had. You two argued about the same three things for eleven months. That wasn't chemistry. That was a pattern.",
            "They're not 'playing hard to get'. They are just not interested. Those are two very different situations with the same ending for you.",
            "You rehearsed what you'd say if they replied. They won't. But go ahead, send the text. At least your 3 AM delusion needs some fresh rejection to grow on.",
            "The energy you're putting into manifesting a text back could power a small country. Direct it anywhere else. Literally anywhere.",
            "You call it love. Any outside observer would call it a parasocial relationship you have with someone who remembers you exist twice a year.",
            "They returned your hoodie. That's a goodbye wrapped in fabric. You kept it as a keepsake. They meant it as a receipt.",
        ],
        "advice": [
            "Put the phone across the room, do not touch it for 20 minutes, and if you still want to embarrass yourself, at least sleep on it first. You almost never regret NOT sending the text.",
            "Delete the thread. Every time you open it you're convincing yourself a past version of reality still exists. It doesn't. You're haunting a house that was demolished.",
            "Go drink water, watch something funny, and text someone who actually wants to hear from you. They exist. Your ex is not that person right now.",
            "The best response to a breakup is getting so aggressively unbothered that your glow-up becomes their problem. Start there.",
            "Write the text in your notes app. Do not send it. Reread it in the morning. Your morning self will be embarrassed at your night self and that's the feedback you need.",
            "If you have to wonder whether you should reach out, the answer is you probably shouldn't. Certainty is a two-way street and they're on a different one.",
        ]
    },
    "study_exam": {
        "tag": "ACADEMIC INTERVENTION",
        "roasts": [
            "So the plan was to defeat the entire semester through the power of doing absolutely nothing until a day before? Fascinating strategy. Statistically suicidal, but fascinating.",
            "You've had three weeks to do this assignment. You chose to remember it exists two hours before it's due. Your time management is a cry for help dressed as a lifestyle.",
            "The syllabus was one document. You read the table of contents and felt like you accomplished something. That's incredible in the worst way.",
            "You spent four hours making a color-coded study schedule and then took a nap to celebrate being organized. You're not organized. You're a performance artist.",
            "Every time you sit down to study you suddenly need to clean your room, reorganize your desk, make tea, and then realize it's been three hours. Your brain has built a whole escape infrastructure.",
            "You're asking me how to absorb a semester's worth of content in ninety minutes. You can't. You're going to walk in there and improvise and we both know it.",
            "You told yourself you work better under pressure. That was a lie you invented in high school to feel better about procrastinating. You don't work better under pressure. Nobody does.",
            "You've watched six YouTube videos titled 'how to study effectively' this week and haven't opened the actual textbook once. That's not studying. That's procrastinating with captions.",
            "The exam is tomorrow and you just asked me what chapter it covers. If you had any survival instincts at all, you'd have known that before today.",
            "You're not a 'last minute person'. You're someone who's never dealt with the anxiety of starting something, so you wait until the anxiety of not finishing it is worse. That's not a personality. That's avoidance.",
            "You pulled an all-nighter, drank enough caffeine to power a data center, and now you're nodding off while 'reviewing'. Your retention rate right now is about four percent. Good luck.",
            "You emailed the professor at 11 PM asking for an extension. That email was sent from the same device you've been using to watch videos all day. That professor knows.",
            "You opened the textbook, read the first sentence, decided the font was uncomfortable, and switched to phone. That's not studying. That's a brief encounter with literature.",
            "Your notes from class say 'important' next to seventeen things and then nothing else. You've been storing confidence instead of information.",
            "You passed last semester by reading summaries the morning of the exam. You're treating that as a strategy instead of a miracle.",
        ],
        "advice": [
            "Stop reading and start doing past exam questions immediately. Active recall beats passive reading every time. You have 90 minutes, use 60 of them on questions not notes.",
            "Email the professor now if it's genuinely an emergency. A short, honest email is better than nothing. Don't invent elaborate excuses — just be direct.",
            "Pick the three highest-weighted topics, do one focused 20-minute block on each, and ignore everything else. You cannot cover everything now. Strategic coverage is your only play.",
            "Put your phone in another room physically. Not face down. In another room. Your concentration span is compromised by having it nearby even if you're not touching it.",
            "Tomorrow: wake up an hour early and read your notes before the exam. Your brain consolidates things during sleep so what you study tonight will actually stick better by morning.",
            "The panic you feel right now is energy. Convert it into targeted action instead of anxious browsing. Twenty minutes of focused work is worth more than three hours of paralyzed scrolling.",
        ]
    },
    "career": {
        "tag": "UNEMPLOYMENT SPEEDRUN",
        "roasts": [
            "You want to quit your stable job to become a content creator with forty followers. Forty. Your own mother and three bots are not a fanbase. They are evidence.",
            "You've been at this company for two years, contributed functionally nothing measurable, and feel you deserve a promotion. That's not ambition. That's entitlement with a LinkedIn bio.",
            "You hate your job but you've spent more time complaining about it than looking for a new one. At this point the job is just an emotional villain in a story where you refuse to become the protagonist.",
            "You're scared of leaving your job because the salary is comfortable. Meanwhile you cry about it every Sunday evening. You're paying for your misery on a subscription basis.",
            "You think you're underpaid but you haven't negotiated once in three years because you're 'not good at confrontation'. Your bank account is also not good at confrontation. See the pattern.",
            "Starting a business based on a voice note idea you had in the shower is not a business plan. That's a daydream with delusions of grandeur.",
            "You want to be your own boss, but you can't finish a personal task without three deadline reminders. Being your own boss requires discipline you're actively refusing to develop.",
            "You're applying to senior roles while your portfolio has one personal project you built in a weekend and abandoned. That gap between expectation and preparation is your whole career arc.",
            "You've been saying you're going to start freelancing for two years. You have not taken a single step. That's not a plan. That's a vibe you're attached to.",
            "You asked your boss for a raise via a three-paragraph Slack message at 5 PM on a Friday. That's not how any of this works.",
            "You get 'nervous in interviews' but won't do mock interviews to practice. You're expecting results from preparation you're unwilling to do. That's just hoping.",
            "You want to be an influencer but you post once every six weeks and delete the video if it gets less than thirty likes. That's not an influencer. That's someone with abandonment issues and a ring light.",
            "You're quitting to travel and find yourself. That's fine. Just know you'll be back in four months, broke, with the same problems and a filtered photo set as the only evidence of personal growth.",
            "You told me your boss is toxic but described an interaction where they just... gave you feedback. I think the toxic one is your ego refusing accountability.",
            "You've rewritten your CV six times in the past month and applied to zero jobs. Perfecting the document is not the same as putting yourself out there. You're procrastinating with formatting.",
        ],
        "advice": [
            "If you want a raise, document three things you demonstrably improved this quarter with numbers, then schedule a 1-on-1 to discuss compensation. That's the only formula that works.",
            "Keep the stable income until the side thing makes at least half of what you currently earn. Then talk about quitting. Quitting first is a romanticized gamble, not a plan.",
            "Apply to five jobs this week. Not research, not rewrite your profile — apply. Five real applications. Momentum is built by action, not by optimizing forever.",
            "Practice interviews out loud, with someone, or in front of your camera. Thinking through answers in your head is not the same as saying them. The gap between what you plan to say and what you actually say under pressure is enormous.",
            "Talk to your manager directly about what growth looks like in this role. Most people don't have this conversation and then are shocked when nothing changes.",
            "Give your side project a 90-day honest effort with defined weekly targets before calling it a business. Most ideas don't survive contact with real effort. That's how you find out which ones do.",
        ]
    },
    "money": {
        "tag": "FINANCIAL DARWINISM",
        "roasts": [
            "You spent your rent money on DoorDash and a memecoin that a TikTok teenager promoted because he called it 'generational wealth'. Your generation of wealth is now minus four hundred dollars.",
            "You say 'money always comes back' but yours hasn't returned since 2022 and it's clearly not planning to. It left. It built a life without you. Let it go.",
            "You have $34 in your account and you're still subscribing to four streaming services you forgot about and a gym membership you've used twice. That's not budgeting. That's financial self-sabotage with aesthetic packaging.",
            "You paid a $26 delivery fee for a $14 meal because you 'didn't feel like cooking'. That math is so wrong it curves back around and becomes a personality flaw.",
            "You bought a luxury item because you 'deserved it' after a hard month. You also can't pay your full phone bill. What you deserve and what you can afford are in a very different conversation.",
            "You're asking me about investing while your savings account has enough for roughly three days of survival. You don't need investment advice. You need a working budget and basic self-control.",
            "You looked at your bank statement, immediately felt sick, closed the app, and ordered food to comfort yourself. You've discovered a feedback loop that ends in bankruptcy.",
            "You're buying things you don't need with money you don't have to impress people who don't think about you. Read that again slowly.",
            "You finance everything. Your phone, your car, your TV, your furniture. Nothing you own is actually yours. You're renting a lifestyle from future you and future you is furious.",
            "You went on a 'treat yourself' shopping trip after vowing to save this month. The vow lasted eight days. That's not a savings plan. That's a delay.",
            "You think going from Starbucks to making coffee at home will fix your finances. That's cute. Your problem is structural, not caffeinated.",
            "You spend money to feel better when you're stressed and you're always stressed about not having money. I want you to really sit with what I just said.",
            "You told me you're 'bad with money' like it's a fixed personality trait and not a learnable skill you've been avoiding for a decade.",
            "You saw something on sale and bought it because saving 30% felt like earning money. You did not earn money. You spent money at a discount. These are different things.",
            "You lent money to someone who still owes you from six months ago and now you're broke. Your friendship is a financial liability.",
        ],
        "advice": [
            "Write down every subscription you have and cancel any you haven't used this month. Not this year. This month. Do it right now before you close this window.",
            "Delete the food delivery apps from your phone's home screen. If you're hungry enough to actually eat, you'll go get food. The apps are for convenience-triggered impulse spending.",
            "Set up a separate account and auto-transfer 10% of every paycheck to it the same day it arrives. Make it annoying to access. Friction is the only way to save.",
            "The 50/30/20 rule: 50% needs, 30% wants, 20% savings. Look at your last month of spending and categorize honestly. Whatever is in the 30% that you regret — that's where your life changes.",
            "Pay off your highest-interest debt first. Every month you wait on that, it's growing. Your future self is paying for your current avoidance.",
            "Tell someone you trust what your financial goal is for the month. Accountability works when the embarrassment of failure is real.",
        ]
    },
    "late_excuse": {
        "tag": "EXCUSE ANNIHILATION",
        "roasts": [
            "You blame your alarm clock like it has a decision-making framework separate from the one you set. You set it wrong. That's on you. The clock executed your instructions flawlessly.",
            "You said traffic was bad. You also left twenty minutes later than you should have. The traffic didn't make you late. Your timeline made you late. Traffic was just there.",
            "You were late because you sat on the edge of your bed wrapped in a towel staring at nothing for thirty five minutes and then panicked. That's not an excuse. That's a confession.",
            "Your assignment was three weeks overdue and you blame your laptop dying. What were you doing during the three weeks before your laptop became the protagonist of your failure?",
            "You told your boss you had food poisoning. You then posted an Instagram story from a restaurant. Your boss saw it. Everyone saw it. You're the food poisoning story now.",
            "The excuse you gave contains four separate unverifiable claims. That's not plausibility. That's an escalating crime scene.",
            "You were late because your 'Uber took forever'. You ordered the Uber seven minutes before the meeting started. You are the cause of every problem in this story.",
            "You told me your WiFi went down. Okay. So you had no phone data, no nearby café, no alternative device, and no way to send a two-sentence heads-up? In 2026? Really?",
            "You missed the deadline because you 'forgot'. You had it written on a sticky note. You had it on your calendar. Your phone sent you a reminder. You forgot in spite of an entire support infrastructure you built and then ignored.",
            "The email you're trying to explain away not sending — you had the tab open. You just didn't send it. Calling that a technical error is genuinely inspiring in how bold it is.",
            "You showed up an hour late and said 'I thought it was at 3'. The invite said 2. You have the invite. You can see it right now. You thought wrong.",
            "You told your professor your grandmother died. It's the third time this year. Either you have a very large and particularly unlucky family, or this is a bold recurring strategy.",
            "You said your car wouldn't start. You drove to get lunch twenty minutes later. The car started. You're the one who didn't.",
            "The excuse required a natural disaster, a failed device, and a medical emergency to even make structural sense. Simpler explanation: you didn't want to be there.",
            "You're not late because of external forces. You're late because something else was more important in that moment and you're not willing to say that out loud.",
        ],
        "advice": [
            "Send a short, honest email right now: 'I'm going to be late because X. I'll have it to you by Y.' No elaboration. No novel. Short, honest, immediate. That's it.",
            "Set your alarm for earlier than you need and put your phone across the room so you physically have to stand up to turn it off. Passive alarms are not the system for you.",
            "If you're consistently late, you're consistently underestimating how long things take. Add 30 minutes to every time estimate you make and you'll be on time.",
            "The best way to not need excuses is to not be late. The best way to not be late is to leave earlier than you think you need to. Simple. Uncomfortable. True.",
            "Own it directly when you're late. 'I underestimated the time, I'm sorry, it won't happen again' works infinitely better than an elaborate excuse nobody fully believes.",
            "If you need a real extension for an assignment, email the professor before the deadline, not after. Same outcome, radically different impression.",
        ]
    },
    "gym_health": {
        "tag": "TERMINAL SLOTH",
        "roasts": [
            "Your fitness routine is walking to the fridge and telling yourself you'll start Monday. It's been 47 consecutive Mondays. Monday is not the problem. You are.",
            "You bought gym clothes six months ago and the only workout they've gotten is absorbing your ambient shame while you scroll TikTok for four hours eating snacks.",
            "You drank one bottle of water today and expect a six pack to materialize. Your hydration and your expectations are both wildly insufficient.",
            "You've said 'I'm going to get in shape' every January for five years. Your New Year self is a liar and your February self knows it.",
            "You spent forty minutes reading about the optimal workout routine instead of just doing any workout. Optimization is your procrastination strategy and it's elegant and useless.",
            "You had one good week at the gym and then missed three weeks and now you're back to 'starting fresh'. You've been starting fresh for two years. You never actually started.",
            "You eat healthy for three days and then have a 'cheat day' that lasts a week and a half. That's not a cheat day. That's your actual diet with a three-day interruption.",
            "You said you don't have time to exercise. You watched four hours of TV yesterday. You have time. You have a preference.",
            "You tried fasting and lasted until 11 AM. You're not built for extremes. Start with one meal that isn't garbage and go from there.",
            "You go to the gym, walk on the treadmill for twenty minutes, take fifteen minutes of selfies, and call it a workout. That's a photo shoot with mild cardio.",
            "You joined an expensive gym to motivate yourself and you haven't gone in three months. The motivation of spending money lasted exactly two weeks. Groundbreaking.",
            "You're not unhealthy because of your genes. You're unhealthy because you treat sleep, food, and movement like optional features rather than basic requirements.",
            "You drink protein shakes but don't exercise. That's not supplementing your fitness. That's just expensive milk with optimistic branding.",
            "You told me you 'don't believe in diets'. That's fine. The vegetables still exist whether you believe in them or not.",
            "You got winded climbing one flight of stairs and decided to sit down. Your body gave you feedback. The feedback was: we need to talk.",
        ],
        "advice": [
            "Don't commit to a six-day gym plan you'll quit by Thursday. Put on shoes and walk outside for 20 minutes today. Consistency is built before intensity. Start there.",
            "Fix one meal a day first. Don't overhaul your entire diet at once — that ends in binging. Replace one bad habit with one better one and give it three weeks to become normal.",
            "Sleep is where your body actually changes. No amount of gym effort survives chronic sleep debt. Fix that first if it's a problem.",
            "The best exercise is the one you'll actually do consistently. Find something you dislike the least and do that instead of planning the perfect regimen you'll never start.",
            "Track what you eat for three days without changing anything. Just write it down. Most people are genuinely shocked at what they discover. Awareness is step one.",
            "Drink water first. It sounds trivial. It's not. Most people's cravings, energy crashes, and headaches are partially dehydration. Start there before anything complex.",
        ]
    },
    "relationship": {
        "tag": "EMOTIONALLY COMPROMISED",
        "roasts": [
            "You described this person as 'complicated' but everything you told me about them sounds like simple disrespect. You've romanticized someone who just doesn't like you that much.",
            "You've been in the talking stage for three months. Either they're the most indecisive person alive or you're not the priority you think you are. Both options require action.",
            "They treat you well 40% of the time and you spend the other 60% earning the good 40% back. That's not a relationship. That's a part-time job with no pay.",
            "You keep saying you're going to have the hard conversation and then don't have it. You're managing their feelings before they've even been expressed. That's not kindness. That's fear.",
            "You changed three major things about yourself to make this person comfortable and they still seem half-interested. You're disappearing and calling it effort.",
            "You justify their behavior every time by finding a reason it makes sense. You are their defense attorney and you didn't even sign up for the role.",
            "You know exactly what they're doing but you're asking me because you want someone to tell you you're wrong. You're not wrong. You already know.",
            "You said 'I don't want to be that person' meaning the person who has standards and expresses them clearly. Being 'that person' is called not tolerating disrespect.",
            "You've been waiting six months for them to 'figure out what they want'. People who want you do not spend six months figuring it out.",
            "You love them more than they love you and you've adjusted your behavior to close that gap instead of acknowledging it exists. That's not sustainable. That's exhausting.",
            "They're not emotionally unavailable. They're available to the right people. You're just not one of them, and that's the sentence you won't say.",
            "You stayed through three red flags and you're calling the fourth one a surprise. It's not a surprise. You just hoped you were the exception. You weren't.",
            "You said 'I don't want to push them away by being too much'. You're already making yourself less to fit into a space that's too small for you.",
            "You're asking if you're being too sensitive. You're not. You're asking the wrong question. The right question is why you're with someone who makes you feel that way.",
            "You give them grace constantly. They give you explanations. Those are not the same thing.",
        ],
        "advice": [
            "Have the actual conversation, out loud, directly. Not over text, not hinted at, not as a joke. Say what you mean and see what happens. You're currently living in a fiction of what might be.",
            "Look at how they behave when things are inconvenient for them. That's who they are. The good moments are real but the moments under pressure are more revealing.",
            "Write down what you actually want from a relationship and then honestly evaluate whether this person is capable of or willing to provide it. Answer honestly to yourself first.",
            "You can love someone and also recognize they are not the right person for you. Those two things can coexist. You don't have to stop caring to start leaving.",
            "Tell someone you trust what's actually happening. You've been carrying this internally and it's distorting your perspective. External clarity is useful right now.",
            "Give this situation a deadline in your head — not an ultimatum you announce, just a personal timeline. If nothing has shifted in 60 days, let that be your information.",
        ]
    },
    "social_media": {
        "tag": "CHRONICALLY ONLINE",
        "roasts": [
            "You've been doom-scrolling for four hours and now you feel anxious, behind, and vaguely ashamed but you're about to do another ten minutes anyway. That's a substance use pattern with better lighting.",
            "You're comparing your actual life to the curated highlight reel of strangers and somehow losing. That's not depression. That's a math error you keep making voluntarily.",
            "You posted something for attention and then spent three hours refreshing to check how much attention it got. The dopamine you chased took three seconds to arrive and three hours of anxiety to process.",
            "You have opinions on fifteen internet conflicts you will never interact with and zero opinions on improving your own immediate circumstances. Interesting allocation of mental energy.",
            "You feel the need to know what's happening in real-time everywhere on the internet at all times. You're not informed. You're overstimulated and calling it awareness.",
            "You got into an argument in the comments section with a stranger about something that will not matter in 48 hours. You won. Congratulations. You're still the same person who did that.",
            "You posted a vague message clearly directed at someone and when they asked if it was about them you said 'no'. You're a passive aggressive performance artist and the audience is confused.",
            "Your screen time is six hours a day and you're wondering why you feel foggy, unmotivated, and like time is slipping. It's slipping. Into your phone. Six hours of it every day.",
            "You're seeking validation from people you don't know about a version of yourself you've curated specifically for them to approve of. That's not connection. That's exhausting theater.",
            "You feel bad about your life every time you open certain apps and you open them constantly. You've identified the problem and chosen not to solve it. That's a choice.",
        ],
        "advice": [
            "Set app limits on the specific apps that drain you. Twenty minutes. When it asks you to extend, close it. The notification can wait. Your mental state is more urgent.",
            "Log off for 48 hours and actually notice how you feel on hour 24 versus hour 1. Most people discover the anxiety decreases rather than increases. Then decide accordingly.",
            "Replace one scroll session per day with something that produces something — anything. Write, cook, exercise, call someone. Consumption versus creation is a meaningful ratio to track.",
            "Unfollow accounts that make you feel bad about yourself. Not because they're wrong, but because the algorithm doesn't care about your emotional state and you have to make decisions for it.",
            "The comparison trap has one solution: stop comparing and start measuring your life against your own previous version. That's the only race worth running.",
            "Put your phone in a drawer from 9 PM to 7 AM for one week. Report back. Seriously. It's not radical. It's just reducing the input.",
        ]
    },
    "procrastination": {
        "tag": "EXPERT AVOIDER",
        "roasts": [
            "You need to do one thing and instead of doing the one thing you've researched how to be more productive, cleaned your entire room, made an elaborate to-do list, and it's now 9 PM.",
            "You keep saying you work better under pressure but you're not producing better work under pressure. You're producing faster work at the same quality and calling the adrenaline satisfaction.",
            "You've convinced yourself that the thinking you're doing about the task is almost the same as doing the task. It is not. It is pure avoidance with intellectual packaging.",
            "You open the document, stare at it, open a new tab, watch a video about someone else doing something productive, and call that a session. Your productivity is entirely vicarious.",
            "You'll start when you feel motivated. Motivation is a consequence of starting, not a prerequisite. You have this backwards and it's why nothing moves.",
            "You have a five-item to-do list. You've reorganized it four times. You've done none of the items. The list is not your problem. Starting is.",
            "You described your procrastination as 'waiting for the right headspace'. Your headspace is never right because doing scary things feels bad before it feels good. Welcome to being alive.",
            "You added a task to your app, set a reminder, made it a habit tracker entry, and felt accomplished. You have not done the task. You have gamified the experience of not doing the task.",
            "You said you'll do it 'later'. Later has never once been a time you actually did the thing. Later is a fiction you tell yourself to feel okay about right now.",
            "You need the perfect conditions to start. The perfect desk, the perfect music, the perfect mood, the perfect lighting, the perfect snack. The task does not care. The task is just waiting.",
        ],
        "advice": [
            "Set a two-minute timer and commit to starting the task for exactly two minutes. Not finishing it. Just starting. Eighty percent of the time you'll continue past two minutes once you've begun.",
            "Pick the smallest possible version of the task and do only that. Not the whole thing. The first paragraph. The first ten minutes. The first five items. Start is the only hard part.",
            "Remove every app from your screen that provides easy distraction while you need to work. Friction to distraction is your best productivity tool. Make the bad habit harder to access.",
            "Tell someone what you're going to do and by when before you start. Accountability is boring and effective. Your internal promises are too easy to renegotiate.",
            "Accept that you won't feel ready and do it anyway. The feeling of being ready is a reward for having started, not a condition for starting. You have this reversed.",
            "Break the task into micro-steps so small they feel embarrassing. 'Open the document' is a step. 'Type the title' is a step. Ridiculous granularity removes the psychological weight of beginning.",
        ]
    },
    "confidence": {
        "tag": "CERTIFIED OVERTHINKER",
        "roasts": [
            "You've rehearsed the conversation in your head forty times and it goes perfectly in your imagination every single time. Reality is going to introduce itself shortly and it won't match.",
            "You're afraid to post something because people might not like it. The people who matter are not refreshing your profile waiting to judge you. They have their own problems.",
            "You've been thinking about starting this for so long that the thinking has become the thing. You're experienced at planning something you've never done.",
            "You care deeply about what people think of you and most of them aren't thinking about you at all. They're thinking about what other people think about them. Everyone is doing this.",
            "You call yourself an introvert to avoid being held responsible for hiding from things that make you anxious. Introversion is about energy, not avoidance. Know the difference.",
            "You said 'I'm not ready yet'. Ready is not a destination you arrive at. It's a feeling that sometimes shows up after you've already started. You've been waiting at the wrong station.",
            "You're smart enough to see every possible way something can go wrong and not brave enough to proceed anyway. That's not intelligence working against you. That's anxiety being mistaken for wisdom.",
            "You self-sabotage right before something good can happen because deep down you don't think you deserve it. That's not humility. That's a belief system that needs to be dismantled.",
            "You need external validation to feel okay about decisions you've already made internally. The outside approval isn't changing your mind. It's just managing your anxiety. Try trusting yourself.",
            "You're playing small because you're scared of the specific kind of failure that comes from actually trying. At least small feels safe. But safe is also exactly what's keeping you stuck.",
        ],
        "advice": [
            "Do the thing badly. Seriously. Give yourself permission to do it imperfectly and let it exist in the world anyway. Bad output that exists beats perfect output that doesn't.",
            "The anxiety before doing something hard is not a signal to stop. It's your nervous system preparing you. You've misread the memo. Feel it and do the thing anyway.",
            "Identify one thing this week that you've been avoiding because you might fail at it. Do that one thing. Not perfectly. Just do it. The data from actually trying is more useful than the theory of possibly trying.",
            "Stop editing yourself before you speak. Say the thing once, see what happens, calibrate after. You're self-censoring based on hypothetical judgment from people who are mostly not paying attention.",
            "Write down three times you did something difficult and it worked out. Your nervous system doesn't store evidence of success the way it stores fear. Make it do the work manually.",
            "Comparison is the specific thing making this worse. Everyone's struggle is invisible on the outside. You're comparing your interior to someone else's exterior and losing. Stop doing that.",
        ]
    },
    "general": {
        "tag": "CASUAL REALITY CHECK",
        "roasts": [
            "Whatever you're going through right now has a 100% chance of being at least partially your fault and a 100% chance of you already knowing that.",
            "You came here for an outside opinion because everyone in your life is too tired to tell you the truth again. I'm not tired. Here's the truth: you already know what you need to do.",
            "I've heard better-reasoned decisions from people who admitted they had no idea what they were doing. At least that's honest.",
            "You're not unlucky. You're making the same decisions in a slightly different font and expecting different results. That's not a rough patch. That's a pattern.",
            "The energy you're putting into explaining this situation could have solved half of it by now. But explaining it feels better than fixing it, so here we are.",
            "You've told this story with yourself as the victim so many times that you've forgotten the part where you had choices. You did. You still do.",
            "I'd tell you to be easier on yourself but honestly the issue is you're being too easy on yourself. A little more accountability would do real work here.",
            "You're not in a difficult situation. You're in a situation you made slightly more difficult by waiting too long to deal with it. Still fixable. Start now.",
            "Everyone has a plan until the plan requires them to do something uncomfortable. Yours fell apart at exactly that point. Predictable. Fixable.",
            "You're catastrophizing something that is genuinely just an inconvenience. Zoom out. This is a problem, not a disaster. Handle it accordingly.",
            "You keep asking for opinions and then arguing with the opinions. You don't want perspective. You want someone to agree with the choice you've already made. So make it and stop asking.",
            "Your problem sounds scary because you haven't started solving it yet. Unsolved problems are always scarier than problems in progress. Start and find out.",
            "You're waiting for it to feel right before you start. It won't feel right until you're already in it. The feeling you're looking for is a consequence, not a condition.",
            "You've described a simple problem using complex emotional language. At the core of this is just a thing you need to do that you don't want to do. Do the thing.",
            "The person you're most frustrated with in this story is you. Everything else is context. That's also the good news — you're the only part of this you can actually change.",
        ],
        "advice": [
            "Take a breath, write down the actual problem in one sentence — not the feelings around it, the actual problem — and then write down one thing you can do today to make it 10% better.",
            "Stop telling the story of the problem and start telling the story of what you're going to do about it. The narrative shift is not just semantic. It changes how you approach it.",
            "Pick the most annoying task on your list, set a 25-minute timer, and just start it. You can stop after 25 minutes. You usually won't want to.",
            "Talk to someone who has actually dealt with this before. Not someone who will sympathize. Someone who has experience. That conversation is worth more than any general advice.",
            "Identify the first obstacle between you and solving this. Not all of them — just the first one. Solve that. Then find the next. Linear progress beats paralysis.",
            "You already know what to do. You're just scared of what happens when you do it. That fear is real and also not a good enough reason to stay stuck.",
        ]
    }
}

# ===========================================================================
# Recent-roast tracking (per process, prevents same-session repeats)
# ===========================================================================
_recent_roasts: list[str] = []
_recent_advice: list[str] = []
MAX_RECENT = 12  # Won't repeat any of the last 12 roasts


def _pick_unique(pool: list[str], recent: list[str]) -> str:
    """Pick a random item from pool, avoiding recent picks."""
    available = [r for r in pool if r not in recent]
    if not available:
        available = pool  # Reset if all exhausted
    choice = random.choice(available)
    recent.append(choice)
    if len(recent) > MAX_RECENT:
        recent.pop(0)
    return choice


def detect_category(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["ex", "girlfriend", "boyfriend", "crush", "dating", "text her", "text him", "breakup",
                             "dumped", "cheated", "talking stage", "situationship", "ghosted", "they haven't replied"]):
        return "ex"
    if any(w in t for w in ["relationship", "partner", "love", "feelings", "emotionally", "communication", "boundaries",
                             "they treat", "they don't", "they keep", "red flag", "toxic relationship"]):
        return "relationship"
    if any(w in t for w in ["study", "studying", "exam", "syllabus", "test", "quiz", "homework", "paper",
                             "assignment", "grade", "fail", "professor", "lecture", "semester", "college", "university"]):
        return "study_exam"
    if any(w in t for w in ["job", "boss", "work", "career", "quit", "resign", "promoted", "streamer", "influencer",
                             "coworker", "salary", "interview", "freelance", "startup", "side hustle", "business"]):
        return "career"
    if any(w in t for w in ["money", "crypto", "bitcoin", "rent", "doordash", "broke", "credit card", "debt",
                             "spent", "gamble", "invest", "stock", "savings", "budget", "afford", "loan", "bills"]):
        return "money"
    if any(w in t for w in ["late", "alarm", "overslept", "forgot", "traffic", "excuse", "missed", "deadline",
                             "didn't show", "couldn't make it", "was running late", "extension"]):
        return "late_excuse"
    if any(w in t for w in ["gym", "diet", "workout", "fat", "weight", "lazy", "exercise", "run", "fitness",
                             "calories", "healthy", "health", "sleep", "protein", "steps"]):
        return "gym_health"
    if any(w in t for w in ["instagram", "tiktok", "twitter", "reddit", "social media", "followers", "likes",
                             "content", "post", "scroll", "online", "chronically", "feed", "algorithm", "screen time"]):
        return "social_media"
    if any(w in t for w in ["procrastinat", "haven't started", "keep putting off", "can't get started",
                             "motivation", "don't feel like", "waiting to feel", "later", "tomorrow", "next week",
                             "haven't done", "still haven't"]):
        return "procrastination"
    if any(w in t for w in ["nervous", "scared", "afraid", "anxious", "anxiety", "confidence", "self-esteem",
                             "shy", "overthink", "what if people", "worried what", "judged", "embarrass",
                             "imposter", "not good enough", "ready yet"]):
        return "confidence"
    return "general"


def generate_fallback_roast(prompt: str, tone: str = "brutal") -> dict:
    category = detect_category(prompt)
    dataset = ROAST_DATABASE.get(category, ROAST_DATABASE["general"])

    roast = _pick_unique(dataset["roasts"], _recent_roasts)
    advice = _pick_unique(dataset["advice"], _recent_advice)

    emotional_damage = random.randint(82, 99)
    delusion_index = random.randint(84, 99)
    copium_level = random.randint(80, 98)

    damage_tier = "💀 SPIRITUALLY EVICTED"
    for min_d, max_d, tier_title, _, _ in DAMAGE_TIERS:
        if min_d <= emotional_damage <= max_d:
            damage_tier = tier_title
            break

    return {
        "roast": roast,
        "ragebait_advice": advice,
        "emotional_damage": emotional_damage,
        "delusion_index": delusion_index,
        "copium_level": copium_level,
        "damage_tier": damage_tier,
        "diagnosis_tag": dataset["tag"],
        # Backward compatibility aliases
        "believability": max(10, 100 - delusion_index),
        "creativity": 92,
        "originality": 88,
        "specificity": 80,
        "plausibility": max(15, 100 - copium_level),
        "desperation": emotional_damage,
        "suspiciousness": delusion_index,
        "bullshit_level": copium_level,
        "overall_score": emotional_damage,
        "verdict": damage_tier,
        "short_reason": roast,
        "detailed_reason": advice,
        "improved_excuse": advice,
        "risk_level": "Rock Bottom"
    }


_DOUBLE_DOWN_ROASTS = [
    "And the fact that you pressed this button instead of going to fix the situation is genuinely your whole personality summarized.",
    "You wanted more? Okay. Your decision-making process is a roulette wheel spun by someone who has never won anything. Go apologize to your future self.",
    "Still here. Waiting for someone to tell you you're fine. You're not fine. That's the whole point. Being fine doesn't require a roast.",
    "You pressed 'Make Me Angrier' because a small part of you thinks you deserve this. That part is right. And it's the most self-aware thing you've done today.",
    "The audacity of pressing this button while the actual problem is still open in another tab.",
    "Real talk: the reason you're here instead of handling it is that handling it requires admitting you have to change something. And you're not ready. But you need to be.",
    "You thought reading another roast would help. Help with what? The roast isn't the therapy. The thing you need to do is. Go do it.",
    "You've now spent more time getting roasted than you would have spent solving the actual issue. That's not entertainment. That's productive avoidance.",
    "Every 'Make Me Angrier' click is another minute you didn't spend fixing anything. At some point you have to stop feeding the beast.",
    "I'm running out of ways to say the same thing differently: you know what needs to happen. The roadblock is willingness, not information.",
    "Honestly? The fact that you need someone to verbally push you this hard to do something you already know you should do is the most revealing thing here.",
    "Congratulations. You've collected two roasts. Would you like to start a collection, or would you like to start a solution?",
]

_recent_double_downs: list[str] = []

def get_double_down_roast(original_roast: str, prompt: str) -> str:
    return _pick_unique(_DOUBLE_DOWN_ROASTS, _recent_double_downs)


# Backward-compatibility wrappers
def calculate_overall_score(believability, creativity, originality, specificity, plausibility, desperation, suspiciousness, bullshit_level):
    return desperation

def get_verdict(overall_score):
    for min_d, max_d, tier_title, short_reason, risk in DAMAGE_TIERS:
        if min_d <= overall_score <= max_d:
            return tier_title, short_reason, risk
    return "💀 SPIRITUALLY EVICTED", "Rock bottom reached.", "Fatal"

def evaluate_fallback(prompt, situation="Other"):
    return generate_fallback_roast(prompt)

def generate_fallback_improved(original_text, situation="Other"):
    roast_data = generate_fallback_roast(original_text)
    return roast_data["ragebait_advice"]
