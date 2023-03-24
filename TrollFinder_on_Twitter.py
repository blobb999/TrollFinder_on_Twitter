import tkinter as tk
import webbrowser
import snscrape.modules.twitter as sntwitter
import tkinter.constants as tk_constants
from constants import SENTINEL_WORDS, AGGRESSIVENESS_WORDS, PRO_TOPICS, CONTRA_TOPICS, PRO_ACCOUNTS, CONTRA_ACCOUNTS
import threading
import csv


stop_scraping = False


def save_to_csv(tweet_data):
    with open('troll_tweets.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Username', 'Tweet URL', 'Reason Type', 'Reason Word']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for tweet in tweet_data:
            writer.writerow(tweet)


def stop_scraping_process():
    global stop_scraping
    stop_scraping = True


def is_trolling(tweet_text):
    lower_tweet_text = tweet_text.lower()

    def check_flag(words):
        return any(word in lower_tweet_text for word in words)

    flags = {
        "sentinel": check_flag(SENTINEL_WORDS),
        "aggressiveness": check_flag(AGGRESSIVENESS_WORDS),
        "pro_topic": check_flag(PRO_TOPICS),
        "contra_topic": check_flag(CONTRA_TOPICS),
        "pro_account": check_flag(PRO_ACCOUNTS),
        "contra_account": check_flag(CONTRA_ACCOUNTS),
    }

    if flags["pro_account"] and (flags["sentinel"] or flags["aggressiveness"]):
        return True
    elif flags["contra_account"] and not (flags["sentinel"] or flags["aggressiveness"]):
        return False
    elif flags["pro_topic"] and not flags["contra_topic"]:
        return True
    elif flags["contra_topic"] and not (flags["sentinel"] or flags["aggressiveness"]):
        return False
    elif flags["sentinel"] or flags["aggressiveness"]:
        return True

    return False


def fetch_tweets(max_tweets):
    hashtag = hashtag_entry.get().strip()
    if not hashtag:
        hashtag = "chemtrails"  # Set default hashtag to chemtrails if no hashtag is entered
    num_tweets = num_tweets_var.get()
    if num_tweets == "All":
        num_tweets = None  # Use None to fetch all available tweets
    else:
        num_tweets = int(num_tweets)  # Convert the string value to an integer

    # Define a function to scrape tweets and check for trolling
    def display_tweets(tweet):
        # Display the troll tweet in the text box
        username = tweet.user.username
        reason = get_troll_reason(tweet.rawContent)

        tweet_textbox.insert(tk.END, f"{username} - ")
        tweet_textbox.insert(tk.END, reason['reason_word'], ('link', get_tweet_thread(tweet)))
        tweet_textbox.insert(tk.END, f" ({reason['reason_type']})\n\n")

        tweet_textbox.tag_config('link', foreground='blue', underline=True)
        tweet_textbox.tag_bind('link', '<Button-1>', lambda e: webbrowser.open_new(tweet_textbox.tag_names(tk.constants.CURRENT)[1]))


    def scrape_tweets():
        i = 0
        troll_tweet_count = 0
        troll_tweets = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"#{hashtag}").get_items()):
            if stop_scraping:
                break

            if num_tweets is not None and i >= num_tweets:
                break

            if max_tweets is not None and troll_tweet_count >= max_tweets:
                break

            # Check if the tweet is trolling
            if is_trolling(tweet.rawContent):
                troll_tweet_count += 1

                # Store the troll tweet data
                troll_tweets.append({
                    'Username': tweet.user.username,
                    'Tweet URL': get_tweet_thread(tweet),
                    'Reason Type': get_troll_reason(tweet.rawContent)['reason_type'],
                    'Reason Word': get_troll_reason(tweet.rawContent)['reason_word']
                })            
                # Display the troll tweet in the text box as it is fetched
                display_tweets(tweet)

            # Update the status label with the number of fetched tweets
            status_label.config(text=f"Fetched {i+1} tweets")
            window.update_idletasks()

        # Update the status label with the number of fetched troll tweets
        status_label.config(text=f"Fetched {troll_tweet_count} troll tweets out of {i+1} tweets")
        window.update_idletasks()

        # Save the troll tweets to a CSV file
        save_to_csv(troll_tweets)        

    def get_tweet_thread(tweet):
        if tweet.conversationId is None:
            return f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
        else:
            return f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"

    def get_troll_reason(tweet_text):
        lower_tweet_text = tweet_text.lower()
        reason = {'reason_type': 'Unknown reason', 'reason_word': ''}

        for word_type, words in [('Sentinel word', SENTINEL_WORDS), ('Aggressiveness word', AGGRESSIVENESS_WORDS)]:
            for word in words:
                if word in lower_tweet_text:
                    reason['reason_type'] = word_type
                    reason['reason_word'] = word
                    return reason

        if any(topic in lower_tweet_text for topic in PRO_TOPICS):
            reason['reason_type'] = 'Pro topic detected'
        elif any(topic in lower_tweet_text for topic in CONTRA_TOPICS):
            reason['reason_type'] = 'Contra topic detected'

        for account in PRO_ACCOUNTS:
            if account.lower() in lower_tweet_text:
                reason['reason_type'] = f"Pro account '{account}' detected"
                break

        return reason

    # Start the scraping process in a new thread
    global stop_scraping
    stop_scraping = False
    scraping_thread = threading.Thread(target=scrape_tweets)
    scraping_thread.start()

# Create the main window
window = tk.Tk()
window.title("Twitter Troll Finder")

# Create the input fields
hashtag_label = tk.Label(window, text="Hashtag:")
hashtag_label.grid(row=0, column=0, padx=5, pady=5)
hashtag_entry = tk.Entry(window)
hashtag_entry.insert(0, "#chemtrails")  # Set default value of hashtag field
hashtag_entry.grid(row=0, column=1, padx=5, pady=5)

num_tweets_label = tk.Label(window, text="Number of Tweets:")
num_tweets_label.grid(row=1, column=0, padx=5, pady=5)
num_tweets_var = tk.StringVar()
num_tweets_var.set("50")
num_tweets_dropdown = tk.OptionMenu(window, num_tweets_var, "50", "100", "All")
num_tweets_dropdown.grid(row=1, column=1, padx=5, pady=5)

# Create the label to display the status
status_label = tk.Label(window, text="")
status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Create the text box to display the troll tweets
tweet_textbox = tk.Text(window, width=50, height=20)
tweet_textbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Create the "Clear" and "Start Scraping" button to clear the text box
start_scraping_button = tk.Button(window, text="Start Scraping", command=lambda: fetch_tweets(100))
start_scraping_button.grid(row=2, column=0, padx=5, pady=5)

clear_button = tk.Button(window, text="Clear", command=lambda: tweet_textbox.delete(1.0, tk.END))
clear_button.grid(row=2, column=1, padx=5, pady=5)

stop_button = tk.Button(window, text="Stop", command=stop_scraping_process)
stop_button.grid(row=2, column=2, padx=5, pady=5)

# Start the GUI loop
window.mainloop()
