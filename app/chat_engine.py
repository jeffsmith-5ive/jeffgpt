
import ast
import operator
import re


class ChatEngine:
    def __init__(self):
        self.letter_map = {number: chr(64 + number) for number in range(1, 27)}
        self.allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

    def get_response(self, messages):
        user_input = self._get_latest_user_input(messages)

        if self._looks_like_decoder_input(user_input):
            return self._decode_numbers_to_text(user_input)

        return self._calculate_expression(user_input)

    def _get_latest_user_input(self, messages):
        for message in reversed(messages):
            if message.get("role") == "user":
                return message.get("content", "")
        return ""

    def _looks_like_decoder_input(self, user_input):
        cleaned = user_input.strip().lower()
        if not cleaned:
            return False

        if cleaned.startswith("decode "):
            return True

        if not re.fullmatch(r"[0-9\s/|]+", cleaned):
            return False

        tokens = re.findall(r"[0-9]+|[\/|]", cleaned)
        has_separator = "/" in cleaned or "|" in cleaned
        has_multiple_numbers = len([token for token in tokens if token.isdigit()]) >= 2
        return has_separator and has_multiple_numbers

    def _decode_numbers_to_text(self, user_input):
        cleaned = user_input.strip().lower()
        if cleaned.startswith("decode "):
            cleaned = cleaned[7:].strip()

        tokens = re.findall(r"[0-9]+|[\/|]", cleaned)
        if not tokens:
            return (
                "Use numbers from 1-26 to decode letters. "
                "Try: 8 9 / 13 25 / 14 1 13 5"
            )

        decoded_parts = []
        current_word = []

        for token in tokens:
            if token in {"/", "|"}:
                if current_word:
                    decoded_parts.append("".join(current_word))
                    current_word = []
                continue

            number = int(token)
            if number == 0:
                if current_word:
                    decoded_parts.append("".join(current_word))
                    current_word = []
                continue

            current_word.append(self.letter_map.get(number, f"[{number}]"))

        if current_word:
            decoded_parts.append("".join(current_word))

        decoded_text = " ".join(decoded_parts)
        if not decoded_text:
            return "I couldn't decode that. Use values from 1-26, with / between words."

        return f"- - {decoded_text}"

    def _calculate_expression(self, user_input):
        cleaned = user_input.strip()
        if not cleaned:
            return "Enter a math problem like 12 / 3 + 4, or a code like 8 9 / 13 25."

        try:
            result = self._safe_eval(cleaned)
        except Exception:
            return (
                "I can calculate math or decode numbers into letters.\n"
                "Math example: 18 * (4 + 2)\n"
                "Decode example: 8 9 / 13 25 / 14 1 13 5"
            )

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return f"Answer: {result}"

    def _safe_eval(self, expression):
        parsed = ast.parse(expression, mode="eval")
        return self._eval_node(parsed.body)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in self.allowed_operators:
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self.allowed_operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in self.allowed_operators:
            operand = self._eval_node(node.operand)
            return self.allowed_operators[type(node.op)](operand)

        raise ValueError("Unsupported expression")
