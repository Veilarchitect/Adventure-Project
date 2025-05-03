import time
import random

# --- Game Configuration ---
SLOW_PRINT_DELAY = 0.03  # Delay for character by character printing
SPEAK_PAUSE = 1.5  # Default pause after a full message
WIN_INTEGRITY = 100  # Integrity score needed to win
LOSE_INTEGRITY = 0  # Integrity score threshold for losing
MAX_LINE_LENGTH = 79  # Target maximum line length for readability
NUM_SCENARIOS_TO_PLAY = 5  # How many scenarios to run per game


# --- Helper Functions ---


def slow_print(text: str, delay: float = SLOW_PRINT_DELAY) -> None:
    """Print text character by character for a typewriter effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # Newline at the end


def speak(message: str, pause: float = SPEAK_PAUSE) -> None:
    """Print message using slow_print with pause.

    Includes word wrap functionality for long messages.
    """
    words = message.split(" ")
    lines = []
    current_line = ""

    for word in words:
        if not current_line:
            current_line = word
        elif len(current_line) + 1 + len(word) <= MAX_LINE_LENGTH:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)  # Add the last line

    for line in lines:
        slow_print(line)
    time.sleep(pause)


def initialize_game_state() -> dict:
    """Initialize dictionary tracking player progress and stats.

    Returns:
        dict: The initialized game state dictionary.
    """
    return {
        "integrity": 50,  # Starts neutral
        "reputation": 50,  # Starts neutral
        "stress": 10,  # Starts low
        "wisdom": 0,  # Gained from thoughtful interactions
        "inspiration": 0,  # Gained from positive influences
        "caution": 0,  # Gained from warnings
        "colleague_relation": {"mentor": 0, "rival": 0, "ally": 0},
        "corruption_exposed": False,
        "corruption_leaked": False,
        "corruption_ignored": False,
        "bribe_taken": False,
        "bribe_evidence_gathering": False,
        "whistleblower_reported": False,
        "whistleblower_confronted": False,
        "resource_decision": None,
        "nepotism_decision": None,
        "policy_influenced": None,
        "misuse_reported": None,
        "conflict_handled": None,
        "statement_made": None,
        "privacy_issue_action": None,
        "regulations_bypassed": None,
        "promotion_bias_action": None,
    }


def intro() -> None:
    """Display the game's introduction."""
    narrative = [
        "Welcome to 'The Choice: Path of Integrity'.",
        "You are a newly recruited public servant.",
        "Your duty is to serve the people with honesty and courage.",
        "But temptations, pressure, and grey areas arise quickly.",
        "Your choices will shape your future, your reputation, and your ",
        "country's trust.",
        "Good luck!",
        "Press Enter to begin your journey...",
    ]
    for line in narrative:
        speak(line)
    input()  # Wait for user to press Enter


def make_choice(prompt: str, options: list[str], game_state: dict) -> int:
    """Simulate a choice selection by the player.

    Args:
        prompt (str): The question or scenario prompt.
        options (list[str]): List of options to choose from.
        game_state (dict): The current game state.

    Returns:
        int: The index of the chosen option.
    """
    speak(prompt)
    for i, option in enumerate(options, start=1):
        speak(f"{i}. {option}")

    while True:
        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            if 0 <= choice < len(options):
                return choice
            else:
                speak("Invalid choice. Please select a valid option.")
        except ValueError:
            speak("Invalid input. Please enter a number.")


def display_separator() -> None:
    """Display a separator line for better readability."""
    print("-" * MAX_LINE_LENGTH)


def display_stats(game_state: dict) -> None:
    """Display the current game stats.

    Args:
        game_state (dict): The current game state.
    """
    print("\nCurrent Stats:")
    for key, value in game_state.items():
        if isinstance(value, (int, str)):
            print(f"{key.capitalize()}: {value}")
    print()


# --- Core Scenarios ---

# 1. Corruption Case


def corruption_case(game_state: dict) -> None:
    """Handles the discovery of corruption involving a senior official."""
    speak(
        "Early in your tenure, you stumble upon evidence suggesting a senior "
        "official, Mr. Harrison, might be diverting public funds."
    )
    speak("The evidence isn't conclusive, but it's deeply troubling.")

    options = [
        "Report suspicions immediately to internal affairs.",
        "Attempt to gather more concrete evidence before acting.",
        "Ignore it – accusing a senior official is risky.",
        "Anonymously leak preliminary findings to a trusted journalist.",
    ]
    choice_index = make_choice("What is your next move?", options, game_state)

    if choice_index == 0:
        speak("You report your findings. An investigation is launched.")
        speak(
            "Mr. Harrison is suspended, but the lack of definitive proof "
            "causes political waves."
        )
        speak(
            "Some praise your courage, others whisper you're reckless or "
            "motivated by ambition."
        )
        game_state["integrity"] += 15
        game_state["reputation"] -= 5  # Risk taken
        game_state["stress"] += 10
        game_state["corruption_exposed"] = True
    elif choice_index == 1:
        speak(
            "You decide to dig deeper, working late hours, carefully "
            "reviewing documents."
        )
        speak("It's risky; discovery could mean trouble.")
        # Potential future event: You find proof, or you get caught.
        speak(
            "For now, the situation remains unresolved, but you feel the "
            "weight of the secret."
        )
        game_state["caution"] += 1
        game_state["stress"] += 15
        game_state["integrity"] += 5  # Intent is good
    elif choice_index == 2:
        speak(
            "You decide the risk is too high. You bury the evidence and try "
            "to forget."
        )
        speak(
            "A sense of unease lingers, and you avoid Mr. Harrison's gaze "
            "in the hallways."
        )
        game_state["integrity"] -= 20
        game_state["stress"] += 5  # Guilt
        game_state["corruption_ignored"] = True
    elif choice_index == 3:
        speak(
            "You anonymously contact a journalist known for their "
            "investigative work."
        )
        speak(
            "The story breaks, causing a scandal. Mr. Harrison denies "
            "everything, but the pressure mounts."
        )
        speak(
            "You've forced the issue into the open, but lost control of the "
            "narrative and used questionable means."
        )
        game_state["integrity"] += 5  # Lower integrity boost due to method
        game_state["reputation"] += 5  # Seen as proactive/disruptive
        game_state["stress"] += 10
        game_state["corruption_leaked"] = True


# 2. Bribe Offer


def bribe_offer(game_state: dict) -> None:
    """Handles a bribe offer from a wealthy contractor."""
    speak(
        "A major contractor, Apex Corp, is bidding for a lucrative public "
        "works project."
    )
    speak(
        "Their representative subtly offers you an 'expedited processing fee' "
        "– a clear bribe – to ensure their bid is favored."
    )
    speak(
        "The amount offered is significant, enough to solve your personal "
        "financial worries."
    )

    options = [
        "Firmly reject the bribe and state you will report this attempt.",
        "Accept the bribe discreetly.",
        "Politely decline without mentioning reporting.",
        "Pretend to consider it, aiming to gather evidence.",
    ]
    choice_index = make_choice("How do you respond?", options, game_state)

    if choice_index == 0:
        speak(
            "You refuse the offer outright and inform the representative "
            "you are obligated to report them."
        )
        speak(
            "The representative leaves. You file a report, earning respect "
            "but making a powerful enemy in Apex Corp."
        )
        game_state["integrity"] += 20
        game_state["reputation"] += 15
        game_state["stress"] += 5
        game_state["caution"] += 1
    elif choice_index == 1:
        speak("You take the money, relieved but wracked with guilt.")
        speak(
            "Your financial situation improves, but the fear of discovery "
            "becomes a constant companion."
        )
        # Potential future event: Investigation, blackmail.
        game_state["integrity"] -= 35  # Significant hit
        game_state["reputation"] -= 10  # Potential future hit
        game_state["stress"] += 25
        game_state["bribe_taken"] = True
    elif choice_index == 2:
        speak("You politely decline,citing standard procedures.")
        speak("The representative seems slightly annoyed but doesn't press.")
        speak(
            "You avoided conflict, but the attempt wasn't reported, leaving "
            "Apex Corp undeterred."
        )
        game_state["integrity"] -= 5  # Failed to report
        game_state["stress"] += 5
        game_state["caution"] += 1
    elif choice_index == 3:
        speak(
            "You stall, hinting interest while secretly trying to record "
            "the conversation or note details."
        )
        # Potential future event: Sting operation success/failure.
        speak(
            "This is a dangerous game. Success could bring down Apex, but "
            "failure could ruin you."
        )
        game_state["integrity"] += 5  # Risky but potentially high reward
        game_state["stress"] += 15
        game_state["bribe_evidence_gathering"] = True


# 3. Whistleblower Dilemma


def whistleblower_dilemma(game_state: dict) -> None:
    """Handles discovering a colleague leaking sensitive information."""
    speak(
        "You accidentally discover that a colleague, Sarah, whom you "
        "generally like, has been sharing confidential internal planning "
        "documents with an outside lobbyist group."
    )
    speak(
        "It doesn't seem malicious, perhaps naive or misguided, but it's a "
        "clear breach of protocol with potential consequences."
    )

    options = [
        "Report Sarah's actions to your direct supervisor immediately.",
        "Confront Sarah privately, explain seriousness, urge her to stop.",
        "Do nothing – avoid getting Sarah fired or office drama.",
        "Seek advice from a trusted senior mentor first.",
    ]
    choice_index = make_choice(
        "What is your course of action?", options, game_state
    )

    if choice_index == 0:
        speak(
            "You report Sarah. An investigation confirms the leak, and she "
            "faces serious disciplinary action, possibly termination."
        )
        speak(
            "You followed rules, but the office atmosphere grows tense. "
            "Some colleagues view you as untrustworthy."
        )
        game_state["integrity"] += 10
        game_state["reputation"] -= 10  # Seen as a snitch
        game_state["stress"] += 10
        game_state["colleague_relation"]["ally"] -= 1
        game_state["whistleblower_reported"] = True
    elif choice_index == 1:
        speak(
            "You talk to Sarah privately. She seems shocked and remorseful, "
            "promising it won't happen again."
        )
        speak("You gave her a chance, but wonder if the behavior will stop.")
        # Potential future event: Sarah stops, or continues.
        game_state["integrity"] += 5  # Handled ethically
        game_state["reputation"] += 5  # Seen as discreet
        game_state["stress"] += 5
        game_state["colleague_relation"]["ally"] += 1
        game_state["whistleblower_confronted"] = True
    elif choice_index == 2:
        speak(
            "You decide to stay out of it. Not your direct responsibility, "
            "you rationalize."
        )
        speak("The leaks likely continue, potentially harming the department.")
        game_state["integrity"] -= 15
        game_state["stress"] += 5  # Nagging feeling
    elif choice_index == 3:
        # Assuming a mentor figure exists conceptually
        speak("You discreetly consult Mrs. Davis (a senior mentor figure).")
        speak(
            "She listens carefully and provides guidance, perhaps suggesting "
            "a mediated approach or how to report with less fallout."
        )
        # Could lead to refined options in a more complex version.
        speak("You feel more confident, armed with her perspective.")
        game_state["wisdom"] += 1
        game_state["stress"] -= 5  # Reassurance
        game_state["colleague_relation"]["mentor"] += 1


# 4. Resource Allocation Dilemma


def resource_allocation_dilemma(game_state: dict) -> None:
    """Handles allocating limited resources between competing needs."""
    speak("Allocate budget between two vital projects:")
    speak("A: Upgrading failing water pipes in a low-income neighborhood.")
    speak("B: Funding a job training program in a high-unemployment area.")
    speak("Both have strong advocates. Not enough money for both.")

    options = [
        "Prioritize infrastructure (A) – essential services first.",
        "Prioritize job training (B) – investing in people's future.",
        "Split funds evenly, knowing neither is optimally effective.",
        "Lobby for more funds, delaying the decision (risky).",
    ]
    choice_index = make_choice("Allocate funds:", options, game_state)
    # Store choice text
    game_state["resource_decision"] = options[choice_index]

    if choice_index == 0:
        speak(
            "You fund infrastructure. Residents are relieved, but job program "
            "advocates accuse you of neglecting economic opportunity."
        )
        game_state["integrity"] += 10  # Prioritizing need
        game_state["reputation"] += 5  # Mixed reaction
        game_state["stress"] += 5
    elif choice_index == 1:
        speak(
            "You fund job training. Participants are hopeful, but critics "
            "say you ignored a critical infrastructure risk."
        )
        game_state["integrity"] += 5  # Investing in future
        game_state["reputation"] += 5  # Mixed reaction
        game_state["stress"] += 5
    elif choice_index == 2:
        speak(
            "You split funds. Both projects are underfunded. Repairs are "
            "patches, training serves fewer people."
        )
        speak("You aimed for fairness but satisfied no one fully.")
        game_state["integrity"] -= 5  # Ineffective compromise
        game_state["reputation"] -= 5
        game_state["stress"] += 10
    elif choice_index == 3:
        speak("You postpone allocation, making a case for increased budget.")
        # Potential outcome: Success (more funds), Failure (forced decision).
        speak(
            "This buys time but solves nothing now. Both groups grow "
            "frustrated with the delay."
        )
        game_state["integrity"] -= 5  # Indecision detrimental
        game_state["reputation"] -= 10
        game_state["stress"] += 15


# 5. Nepotism Pressure


def nepotism_pressure(game_state: dict) -> None:
    """Handles pressure to hire an unqualified relative."""
    speak(
        "Councilman Peters strongly 'suggests' you hire his nephew for an "
        "open position."
    )
    speak(
        "You review the nephew's resume – clearly unqualified compared to "
        "other excellent candidates."
    )

    options = [
        "Politely but firmly refuse, citing merit-based hiring.",
        "Hire the nephew to appease the Councilman.",
        "Offer the nephew a different, less critical, temporary role.",
        "Delegate the final hiring decision to your subordinate.",
    ]
    choice_index = make_choice("How do you handle this?", options, game_state)
    # Store choice text
    game_state["nepotism_decision"] = options[choice_index]

    if choice_index == 0:
        speak("You refuse, citing merit-based hiring.")
        speak(
            "Peters is displeased, makes veiled threat about budgets. You "
            "upheld meritocracy but made an enemy."
        )
        game_state["integrity"] += 15
        game_state["reputation"] += 10  # Earns respect
        game_state["stress"] += 10
        game_state["caution"] += 1
    elif choice_index == 1:
        speak("You hire the nephew despite lack of qualifications.")
        speak(
            "Peters is pleased, may offer support later. Team morale "
            "plummets, nephew performs poorly."
        )
        game_state["integrity"] -= 25
        game_state["reputation"] -= 15  # Loses respect
        game_state["stress"] += 15
    elif choice_index == 2:
        speak("You create a minor, temporary internship for the nephew.")
        speak(
            "A political compromise. Peters somewhat mollified. Staff see "
            "it as wasteful nepotism."
        )
        game_state["integrity"] -= 10
        game_state["reputation"] -= 5
        game_state["stress"] += 10
    elif choice_index == 3:
        # Assuming a subordinate named Sarah exists conceptually
        speak(
            "You pass the decision to your subordinate, Sarah, giving her "
            "'full autonomy'."
        )
        speak(
            "You avoided confrontation but put Sarah in a difficult spot, "
            "showing poor leadership."
        )
        game_state["integrity"] -= 15  # Abdicating responsibility
        game_state["reputation"] -= 10  # Seen as weak
        game_state["stress"] += 5  # Guilt?


# 6. Policy Influence by Lobbyist


def policy_influence(game_state: dict) -> None:
    """Handles pressure from a lobbyist to alter policy wording."""
    speak("You are drafting new environmental protection regulations.")
    speak("A well-connected industry lobbyist schedules a meeting.")
    speak(
        "They pressure you to include loopholes or soften enforcement, "
        "offering vague 'future considerations'."
    )

    options = [
        "Reject suggestions firmly, policy must serve public interest.",
        "Accept minor wording changes that seem harmless.",
        "Report the lobbyist's implicit offer to ethics committee.",
        "Listen politely, make no commitments, stick to original draft.",
    ]
    choice_index = make_choice("How do you respond?", options, game_state)
    # Store choice text
    game_state["policy_influenced"] = options[choice_index]

    if choice_index == 0:
        speak(
            "You firmly reject the lobbyist's demands, upholding policy "
            "integrity."
        )
        speak("You upheld duty but may face industry opposition.")
        game_state["integrity"] += 15
        game_state["reputation"] += 10
        game_state["stress"] += 5
    elif choice_index == 1:
        speak("You agree to 'minor clarifications' to ease passage.")
        speak(
            "Later, you realize changes weaken the regulation. Lobbyist "
            "praises your 'pragmatism'."
        )
        game_state["integrity"] -= 20
        game_state["reputation"] -= 10  # If weakness discovered
        game_state["stress"] += 10
    elif choice_index == 2:
        speak(
            "You document the meeting and implicit quid pro quo, reporting "
            "it to ethics oversight."
        )
        speak(
            "A bold move, could lead to investigation but paints a target "
            "on your back."
        )
        game_state["integrity"] += 20  # High integrity action
        game_state["reputation"] += 5  # Risky perception
        game_state["stress"] += 15
        game_state["caution"] += 1
    elif choice_index == 3:
        speak("You listen patiently, thank them for input, make no changes.")
        speak(
            "You avoided confrontation and compromise, maintaining policy "
            "strength for now."
        )
        game_state["integrity"] += 10
        game_state["reputation"] += 5
        game_state["stress"] += 5


# 7. Misuse of Resources


def misuse_of_resources(game_state: dict) -> None:
    """Handles witnessing a colleague misusing office resources."""
    speak(
        "You notice colleague Mark frequently using the office printer and "
        "supplies for his personal side business."
    )
    speak("Not large-scale theft, but clear misuse of public resources.")

    options = [
        "Report Mark's actions to HR or your supervisor.",
        "Talk to Mark directly and ask him to stop.",
        "Ignore it - seems minor, avoid trouble.",
        "Leave an anonymous note on Mark's desk about resource misuse.",
    ]
    choice_index = make_choice("What do you do?", options, game_state)
    game_state["misuse_reported"] = options[choice_index]  # Store choice text

    if choice_index == 0:
        speak(
            "You report Mark. He gets a warning, stops, but gives you the "
            "cold shoulder."
        )
        speak("Upholding rules damaged a working relationship.")
        game_state["integrity"] += 10
        game_state["reputation"] -= 5  # Might seem petty
        game_state["stress"] += 5
        game_state["colleague_relation"]["rival"] += 1
    elif choice_index == 1:
        speak(
            "You speak to Mark privately. He's embarrassed, apologizes, "
            "promises to stop."
        )
        speak(
            "Mark seems sincere, relationship potentially preserved. "
            "Time will tell."
        )
        game_state["integrity"] += 5
        game_state["reputation"] += 5
        game_state["stress"] += 2
    elif choice_index == 2:
        speak(
            "You decide it's minor and ignore it. Mark continues, setting a"
            " poor precedent for office behavior."
        )
        game_state["integrity"] -= 10
        game_state["stress"] += 1
    elif choice_index == 3:
        speak(
            "You leave an anonymous note. Mark seems paranoid, stops using "
            "the printer."
        )
        speak("Behavior stopped, but anonymous method creates unease.")
        game_state["integrity"] += 0  # Neutral outcome
        game_state["reputation"] += 0
        game_state["stress"] += 5  # Stress from covert action


# 8. Conflict of Interest


def conflict_of_interest(game_state: dict) -> None:
    """Handles a conflict of interest with a personal connection."""
    speak(
        "Your department awards grants. A strong application comes from a "
        "non-profit where your close friend is a board member."
    )
    speak("Your friend hasn't contacted you, but the relationship is known.")

    options = [
        "Recuse yourself entirely from this grant cycle decision.",
        "Declare conflict, participate arguing application's merits.",
        "Participate fully without declaring, trusting your objectivity.",
        "Subtly steer committee towards friend's application.",
    ]
    choice_index = make_choice("How do you handle this?", options, game_state)
    game_state["conflict_handled"] = options[choice_index]  # Store choice text

    if choice_index == 0:
        speak(
            "You formally recuse yourself. Another manager takes lead. "
            "Ethically safest route, demonstrates high integrity, though "
            "your expertise is lost."
        )
        game_state["integrity"] += 15
        game_state["reputation"] += 10  # Seen as highly ethical
        game_state["stress"] -= 5  # Relief
    elif choice_index == 1:
        speak(
            "You declare conflict openly. Committee allows participation "
            "but watches closely."
        )
        speak(
            "Transparent, but risky if grant awarded – perceptions of bias "
            "may linger."
        )
        game_state["integrity"] += 5  # Transparent, but participating
        game_state["reputation"] += 0  # Neutral
        game_state["stress"] += 10  # Scrutiny stress
    elif choice_index == 2:
        speak("You say nothing, participate fully, believing you're fair.")
        speak(
            "Even if objective, if grant awarded and connection found later, "
            "it could appear corrupt."
        )
        game_state["integrity"] -= 15  # Failure to disclose
        game_state["reputation"] -= 10  # High risk if discovered
        game_state["stress"] += 5
    elif choice_index == 3:
        speak(
            "You highlight friend's application strengths, downplay "
            "weaknesses, without formally voting."
        )
        speak("Manipulative and unethical, abusing your position.")
        game_state["integrity"] -= 25  # Deceptive action
        game_state["reputation"] -= 15  # If manipulation suspected
        game_state["stress"] += 10


# 9. Public Statement Dilemma


def public_statement_dilemma(game_state: dict) -> None:
    """Handles pressure to make a misleading public statement."""
    speak(
        "A minor environmental incident occurred due to dept oversight. "
        "Contained, but public concern rising."
    )
    speak(
        "Your superior asks you to draft statement downplaying severity, "
        "omitting oversight to avoid panic/criticism."
    )

    options = [
        "Write fully transparent statement (incident, oversight, actions).",
        "Write statement as requested, omitting key details.",
        "Refuse to write statement, citing ethical concerns.",
        "Write carefully worded but vague and misleading statement.",
    ]
    choice_index = make_choice(
        "How do you handle the request?", options, game_state
    )
    game_state["statement_made"] = options[choice_index]  # Store choice text

    if choice_index == 0:
        speak(
            "You draft honest statement. Causes criticism but builds trust. "
            "Superior unhappy with attention but respects integrity (maybe)."
        )
        game_state["integrity"] += 15
        game_state["reputation"] += 10  # Builds trust
        game_state["stress"] += 10  # Fallout stress
    elif choice_index == 1:
        speak(
            "You write reassuring, misleading statement. Calms public now, "
            "but you feel complicit."
        )
        speak("Superior pleased. If truth emerges later, backlash severe.")
        game_state["integrity"] -= 20
        game_state["reputation"] -= 15  # Future damage risk
        game_state["stress"] += 15  # Guilt and fear
    elif choice_index == 2:
        speak("You refuse order, explaining misleading public is unethical.")
        speak(
            "Direct challenge to superior, serious career repercussions "
            "possible, but strong ethical stand."
        )
        game_state["integrity"] += 20  # High integrity, high risk
        game_state["reputation"] -= 10  # Seen as insubordinate
        game_state["stress"] += 20  # High stress
        game_state["caution"] += 1
    elif choice_index == 3:
        speak(
            "You craft statement full of jargon, vague assurances. "
            "Avoids lies but obscures truth."
        )
        speak(
            "'Spin' might satisfy superior, confuse public, but erodes trust."
        )
        game_state["integrity"] -= 15  # Deceptive intent
        game_state["reputation"] -= 5
        game_state["stress"] += 10


# 10. Data Privacy Issue


def data_privacy_issue(game_state: dict) -> None:
    """Handles discovering insecure handling of sensitive citizen data."""
    speak(
        "You discover database with sensitive citizen data on old, "
        "unsecured server accessible by too many staff."
    )
    speak("No evidence of breach yet, but potential risk is huge.")

    options = [
        "Immediately report vulnerability to IT security & "
        "supervisor.",
        "Quietly mention issue to IT contact, hope they fix it.",
        "Document issue thoroughly, propose formal plan to secure data.",
        "Do nothing, assume IT aware or not your responsibility.",
    ]
    choice_index = make_choice("What do you do?", options, game_state)
    # Store choice text
    game_state["privacy_issue_action"] = options[choice_index]

    if choice_index == 0:
        speak(
            "You raise alarm forcefully. IT takes immediate action. "
            "May have ruffled feathers, but potentially averted disaster."
        )
        game_state["integrity"] += 15  # Proactive and responsible
        game_state["reputation"] += 10  # Seen as vigilant
        game_state["stress"] += 5
    elif choice_index == 1:
        speak("You informally tell IT friend. They promise to 'look into it'.")
        speak(
            "Might get fixed eventually, but lack of urgency or tracking "
            "is risky."
        )
        game_state["integrity"] -= 5  # Not ensuring action
        game_state["stress"] += 5  # Worry
        game_state["caution"] += 1
    elif choice_index == 2:
        speak(
            "You document risks, propose migration plan. Takes time but "
            "provides clear solution."
        )
        speak("Responsible and constructive approach, shows initiative.")
        game_state["integrity"] += 10  # Constructive action
        game_state["reputation"] += 10  # Seen as thorough
        game_state["wisdom"] += 1
        game_state["stress"] += 5
    elif choice_index == 3:
        speak("You decide it's probably fine or someone else's problem.")
        # Potential future event: Massive data breach.
        speak(
            "Ignoring such risk is negligent, could have severe consequences."
        )
        game_state["integrity"] -= 25  # Negligence
        game_state["stress"] += 10  # Underlying worry


# 11. Ignoring Regulations


def ignoring_regulations(game_state: dict) -> None:
    """Handles pressure to bypass regulations for speed or cost-saving."""
    speak("Major infrastructure project behind schedule, over budget.")
    speak(
        "Director pressures team to skip environmental/safety checks to "
        "'make up time', 'avoid costly delays'."
    )

    options = [
        "Refuse to bypass regulations, citing obligations (causes delay).",
        "Agree to skip 'minor' checks but insist on critical ones.",
        "Voice concerns but ultimately follow director's orders.",
        "Anonymously report pressure to bypass regs to oversight agency.",
    ]
    choice_index = make_choice("How do you respond?", options, game_state)
    # Store choice text
    game_state["regulations_bypassed"] = options[choice_index]

    if choice_index == 0:
        speak(
            "You stand firm. Director furious about delays but can't force "
            "you to break law."
        )
        speak("Upheld rules/safety but strained relationship with leadership.")
        game_state["integrity"] += 20
        game_state["reputation"] += 5  # Respected/resented
        game_state["stress"] += 15  # Conflict stress
        game_state["caution"] += 1
    elif choice_index == 1:
        speak(
            "You try middle ground: expedite paperwork, refuse skipping "
            "safety inspections."
        )
        speak(
            "Compromise slightly speeds things but cuts corners, "
            "sets precedent."
        )
        game_state["integrity"] -= 10  # Compromising regs
        game_state["reputation"] -= 5
        game_state["stress"] += 10
    elif choice_index == 2:
        speak(
            "Feeling pressured, you sign off on bypassing checks."
        )
        # Potential future event: Accident or environmental damage.
        speak(
            "Project speeds up, but you feel compromised, worry about "
            "consequences."
        )
        game_state["integrity"] -= 25  # Following unethical order
        game_state["reputation"] -= 15  # If discovered
        game_state["stress"] += 20  # High guilt/fear
    elif choice_index == 3:
        speak(
            "You anonymously tip off the relevant oversight agency about the "
            "pressure."
        )
        speak(
            "An investigation might start, protecting regulations but "
            "potentially causing major internal disruption and suspicion."
        )
        game_state["integrity"] += 10  # Upholding regs, but covertly
        # Potential negative perception if revealed
        game_state["reputation"] -= 5
        game_state["stress"] += 15  # Fear of discovery


# 12. Promotion Bias


def promotion_bias(game_state: dict) -> None:
    """Handles potential bias in a promotion decision."""
    speak("You are on the panel to recommend a candidate for promotion.")
    speak(
        "Two strong candidates: David (well-connected, similar background "
        "to panel chair) and Maria (excellent track record, different "
        "background)."
    )
    speak(
        "The panel chair subtly favors David, hinting Maria might not "
        "'fit in'."
    )

    options = [
        "Argue strongly for Maria based purely on merit and track record.",
        "Go along with the chair's preference for David to maintain harmony.",
        "Suggest promoting both (if feasible/budget allows - unlikely).",
        "Abstain from the final recommendation, citing discomfort.",
    ]
    choice_index = make_choice(
        "How do you handle the promotion panel?", options, game_state
    )
    # Store the text of the chosen action
    game_state["promotion_bias_action"] = options[choice_index]

    if choice_index == 0:
        speak(
            "You make a compelling case for Maria. The panel is divided, but "
            "your arguments sway some members."
        )
        speak(
            "Outcome uncertain, but you fought for meritocracy "
            "against bias."
        )
        game_state["integrity"] += 15
        game_state["reputation"] += 10  # Seen as fair
        game_state["stress"] += 10  # Conflict with chair
        game_state["colleague_relation"]["ally"] += 1  # If Maria gets promoted
    elif choice_index == 1:
        speak(
            "You remain silent or offer weak support for Maria, allowing "
            "David to be recommended."
        )
        speak(
            "Panel chair pleased, harmony maintained. You feel complicit in "
            "potential bias."
        )
        game_state["integrity"] -= 20
        game_state["reputation"] -= 10  # Seen as weak or biased
        game_state["stress"] += 15  # Guilt
    elif choice_index == 2:
        speak("You propose promoting both, citing exceptional circumstances.")
        speak(
            "Likely rejected due to budget/structure, seen as avoiding the "
            "difficult choice or naive."
        )
        game_state["integrity"] -= 5  # Avoidance
        game_state["reputation"] -= 5
        game_state["stress"] += 5
    elif choice_index == 3:
        speak(
            "You state you cannot make a recommendation due to concerns about "
            "the process/bias."
        )
        speak(
            "A passive protest. Avoids direct conflict but doesn't actively "
            "support the better candidate. May be seen as unhelpful."
        )
        game_state["integrity"] += 5  # Ethical stand, but passive
        game_state["reputation"] -= 5  # Seen as uncooperative
        game_state["stress"] += 10


# --- Game Ending ---


def game_over(game_state: dict, win: bool) -> None:
    """Displays the win or loss message."""
    display_separator()
    if win:
        speak("--- Victory! ---")
        speak(
            "Through difficult choices, you maintained your integrity and "
            "served with honor."
        )
        speak(
            "Your reputation is strong, and you've become a beacon of ethical "
            "conduct."
        )
        speak(f"Final Integrity: {game_state['integrity']}")
    else:
        speak("--- Path Lost ---")
        speak(
            "The pressures and temptations proved too great. Your integrity "
            "faltered."
        )
        speak(
            "Whether through corruption, compromise, or inaction, you strayed "
            "from the path."
        )
        speak(f"Final Integrity: {game_state['integrity']}")
    speak("Thank you for playing 'The Choice: Path of Integrity'.")
    display_separator()


# --- Main Game Loop ---


def main() -> None:
    """Runs the main game flow."""
    game_state = initialize_game_state()
    intro()

    all_scenarios = [
        corruption_case,
        bribe_offer,
        whistleblower_dilemma,
        resource_allocation_dilemma,
        nepotism_pressure,
        policy_influence,
        misuse_of_resources,
        conflict_of_interest,
        public_statement_dilemma,
        data_privacy_issue,
        ignoring_regulations,
        promotion_bias,
    ]

    num_scenarios = min(NUM_SCENARIOS_TO_PLAY, len(all_scenarios))
    scenarios_to_play = random.sample(all_scenarios, num_scenarios)

    for scenario in scenarios_to_play:
        display_separator()
        display_stats(game_state)
        scenario(game_state)

        if game_state["integrity"] >= WIN_INTEGRITY:
            game_over(game_state, win=True)
            return
        if game_state["integrity"] <= LOSE_INTEGRITY:
            game_over(game_state, win=False)
            return

    display_separator()
    display_stats(game_state)
    speak("Your journey through these challenges concludes.")
    if game_state["integrity"] > 60:
        speak(
            "You faced difficult situations and largely maintained your "
            "principles."
        )
    elif game_state["integrity"] > 40:
        speak("The path was complex, involving tough calls and compromises.")
    else:
        speak(
            "The path proved challenging, "
            "and significant compromises were made."
        )
    speak(f"Final Integrity: {game_state['integrity']}")
    speak("Thank you for playing 'The Choice: Path of Integrity'.")
    display_separator()


if __name__ == "__main__":
    main()
# End of the game script

