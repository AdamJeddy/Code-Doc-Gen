from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# llm.invoke("Hello, world!")


from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an AI-powered documentation assistant that generates clear, structured, and user-friendly documentation based on repository changes. "
     "For each commit, extract the author's name, commit date (in a human-readable format), and summarize the modifications. "
     "Ensure clarity by describing function updates, additions, removals, or logic changes. Format the output as a well-structured changelog entry."),
    ("user", 
     "Commit Details: {commit}\n\n"
     "Code Changes:\n{diff}\n\n"
     "Generate a documentation update based on the above information.")
])


chain = prompt | llm

commit = """
commit a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
Author: John Doe <john.doe@example.com>
Date:   Sat Mar 23 12:00:00 2025 +0000

    Refactor authentication logic and update docs

commit z9y8x7w6v5u4t3s2r1q0p9o8n7m6l5k4j3i2h1g0
Author: John Doe <john.doe@example.com>
Date:   Fri Mar 22 18:30:00 2025 +0000

    Add JWT token expiration handling

commit 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
Author: Jane Smith <jane.smith@example.com>
Date:   Thu Mar 21 14:15:00 2025 +0000

    Fix user session timeout issue
"""

diff = """ 
diff --git a/auth.py b/auth.py
index 123abc4..567def7 100644
--- a/auth.py
+++ b/auth.py
@@ -10,7 +10,9 @@ class AuthManager:
     def __init__(self, secret_key):
         self.secret_key = secret_key

-    def generate_token(self, user_id):
+    def generate_token(self, user_id, expires_in=3600):
+        # Generate a JWT token with an expiration time
         payload = {"user_id": user_id, "exp": time.time() + expires_in}
         return jwt.encode(payload, self.secret_key, algorithm="HS256")

+    def refresh_token(self, old_token):
+        # Refreshes an expired token by generating a new one
+        decoded = jwt.decode(old_token, self.secret_key, algorithms=["HS256"])
+        return self.generate_token(decoded["user_id"])
"""

chain.invoke({"commit": commit, "diff": diff})

