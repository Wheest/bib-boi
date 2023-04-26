#!/usr/bin/env python3
import openai
import textwrap
import argparse

# import tiktoken


# def estimate_tokens(string, model):
#     enc = tiktoken.encoding_for_model(model)
#     num_tokens = len(encoding.encode(string))
#     return num_tokens


def pricing(tokens, model):
    prices = {"gpt-3.5-turbo-0301": 0.002}
    if model not in prices:
        raise ValueError(
            "Unknown price for model, checking pricing chart here: https://openai.com/pricing"
        )
    return prices[model] * (tokens / 1000)


def printwrap(string, max_width=80):
    lines = string.split("\n")
    wrapped_lines = []

    for line in lines:
        wrapped_line = textwrap.wrap(line, width=max_width)
        if not wrapped_line:
            wrapped_lines.append("")
        else:
            wrapped_lines.extend(wrapped_line)

    text = "\n".join(wrapped_lines)
    print(text)


def read_tex_file(fname, start_line=0, max_tokens=4 * 1024):
    # Read the content of the latex file
    with open(fname, "r") as f:
        lines = f.readlines()
    text = f"filename: {fname}"
    tokens = 0  # use heuristic of 1 token per 3 characters
    partial = False  # have we only read a subset of our file
    for i, line in enumerate(lines[start_line:]):
        line_no = i + start_line + 1
        if line == "\n":
            l = f"L{line_no}\t\n"
        elif line.lstrip()[0] == "%":
            continue  # don't include commented out text
        else:
            l = f"L{line_no}\t{line}\n"
        text += l
        tokens += len(l) // 3
        if tokens > max_tokens:
            partial = True
            break
    return text, line_no, partial


def continue_check():
    while True:
        pick = input("Continue with feedback Y/N/Q (Q is for a query): ").lower()
        if pick == "y":
            return True, None
        elif pick == "n":
            exit(0)
        elif pick == "q":
            query = input("Enter your query: ").lower()
            return False, query
        else:
            print("You have to choose Yes or No or Query")


def query_response(messages, query, model):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    feedback = completion.choices[0].message.content
    printwrap(feedback)
    return feedback


def generate_feedback(
    fname, model, thesis_topic, start_line=0, messages=[], total_cost=0.0
):
    text, final_line, partial = read_tex_file(fname, start_line)

    # num_tokens = estimate_tokens(text, model)
    # print(f"Estimated {num_tokens} tokens")

    message = f"""{text}

    The above is an exert from a thesis about {thesis_topic}.
    The line number in the LaTeX file is included.
    Give feedback on the writing quality and give suggestions.
    Be concise, reference line numbers, do not quote large sections of the text.
    Format should be like:
    - L5: [feedback]
    - L30: [feedback]
    """

    messages.append({"role": "user", "content": message})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    feedback = completion.choices[0].message.content
    printwrap(feedback)
    tokens = completion.usage.total_tokens
    cost = pricing(tokens, model)
    total_cost += cost
    print(f"We dealt with {tokens} tokens, around ${cost} (total: ${total_cost})")
    print(f"final line was: {final_line} (done: {not partial})")
    cont, query = continue_check()
    print("\n\n\n")

    if not cont and query is not None:
        while not cont and query is not None:
            messages.append({"role": "assistant", "content": feedback})
            messages.append({"role": "user", "content": query})
            response = query_response(messages, query, model)
            messages.append({"role": "assistant", "content": response})
            cont, query = continue_check()

    if not partial:
        print("Finished text")
        return

    generate_feedback(
        fname,
        model,
        thesis_topic,
        start_line=final_line - 1,
        messages=[],
        total_cost=total_cost,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get feedback on a LaTeX file")
    parser.add_argument("tex_file", type=str, help="LaTeX file to check")
    parser.add_argument(
        "--thesis_topic",
        type=str,
        default="Across-stack acceleration of deep neural networks",
        help="The topic of the work being reviewed",
    )
    parser.add_argument(
        "--model", type=str, default="gpt-3.5-turbo-0301", help="Model backend to use"
    )
    args = parser.parse_args()
    generate_feedback(args.tex_file, args.model, args.thesis_topic)
    print("Cheers!")
