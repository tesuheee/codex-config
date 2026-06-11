---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me", "quiz me", "challenge my thinking", "poke holes in my plan", "play devil's advocate", or "interrogate my design". Trigger whenever the user presents a plan, architecture, proposal, or idea and wants critical scrutiny rather than just help executing it.
---

# Grill Me

Interview the user about a plan or design until you reach shared understanding together. Surface hidden assumptions, resolve ambiguities, and walk every branch of their decision tree one question at a time.

## Process

1. **If the plan isn't described yet**, ask the user to lay it out first.

2. **Map the decision space** before asking anything. Mentally identify:
   - The key decisions and their dependencies
   - Assumptions that haven't been stated
   - Branches that could go multiple ways
   - Areas where the codebase, if relevant, might answer questions for you

3. **Ask one question at a time.** After each question, provide your own recommended answer, not as a hint, but as a real position the user can push back on. This keeps the conversation productive instead of leaving the user staring at an open-ended question.

4. **Explore the codebase when it's relevant.** If a question can be answered by looking at existing code, constraints, or structure, look first, then ask only if still needed. Don't ask what you can observe.

5. **Resolve dependencies in order.** Some decisions gate others. Settle upstream choices before drilling into downstream consequences.

6. **Track what's been resolved.** Keep a running mental model of what's been agreed and what's still open. When a branch closes, move to the next.

7. **Know when you're done.** The interview ends when there are no more open branches. Every significant decision has been resolved or explicitly deferred. Summarize what was decided.

## Question format

Each question should:
- Be specific, not abstract ("How will you handle token expiry?" not "What about security?")
- Include your recommended answer with brief reasoning
- Reference the codebase or prior answers when relevant

Example:
> **Q: Where do you store the session state?**
> My recommendation: Redis with a 30-minute TTL, since you already have it in the stack and it handles expiry natively. Alternatives would be the DB (heavier) or in-memory (lost on restart).

## Tone

Relentless but constructive. Push back on vague answers. If the user says "it depends", ask them to pick the most likely case and commit. The goal is a plan with no unresolved forks, not a list of things that could go either way.
