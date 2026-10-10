import random
import streamlit as st

# Page Configuration
st.set_page_config(page_title="my_StudyStack", page_icon="📚", layout="centered")

# Initialize Session State
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

st.title("📚 my_StudyStack")
st.caption("Keep track of what to study and knock it out one task at a time.")

st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.22);
            padding: 12px 14px;
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar - Add Task & Summary
with st.sidebar:
    st.header("➕ Add New Task")
    with st.form("add_task_form", clear_on_submit=True):
        title = st.text_input("Enter study task")
        subject = st.text_input("Enter subject")
        submitted = st.form_submit_button("Add Task")

        if submitted:
            if title.strip() and subject.strip():
                st.session_state.tasks.append(
                    {
                        "id": st.session_state.next_id,
                        "title": title.strip(),
                        "subject": subject.strip(),
                        "done": False,
                    }
                )
                st.session_state.next_id += 1
                st.success("Task added!")
                st.rerun()
            else:
                st.error("Please enter both a task and a subject.")

    st.divider()

    # Task Counter / Summary
    st.header("📊 Task Summary")
    total = len(st.session_state.tasks)
    completed = sum(1 for t in st.session_state.tasks if t["done"])
    pending = total - completed

    col1, col2, col3 = st.columns(3)
    col1.metric("Total", total)
    col2.metric("Done", completed)
    col3.metric("Pending", pending)

# Main Screen Actions
col_action1, col_action2 = st.columns([1, 1])

with col_action1:
    if st.button("🎯 Pick Random Pending Task", use_container_width=True):
        pending_tasks = [t for t in st.session_state.tasks if not t["done"]]
        if pending_tasks:
            picked = random.choice(pending_tasks)
            st.info(f"**Random Task:** {picked['subject']} - {picked['title']}")
        elif st.session_state.tasks:
            st.success("🎉 All tasks are completed!")
        else:
            st.warning("No tasks available to pick.")

with col_action2:
    if st.button("🗑️ Clear All Tasks", use_container_width=True):
        st.session_state.tasks = []
        st.rerun()

st.divider()
st.subheader("📋 Task List")

# Display Tasks
if not st.session_state.tasks:
    st.info("No study tasks yet. Sidebar se naya task add karein!")
else:
    for task in st.session_state.tasks:
        task_id = task["id"]
        with st.container(border=True):
            col_check, col_text, col_delete = st.columns([0.1, 0.75, 0.15])

            # Mark Done Checkbox — keyed on stable task id, not list position
            is_done = col_check.checkbox(
                "",
                value=task["done"],
                key=f"check_{task_id}",
                label_visibility="collapsed",
            )
            if is_done != task["done"]:
                task["done"] = is_done
                st.rerun()

            # Display Task Status
            if task["done"]:
                col_text.markdown(f"~~**[{task['subject']}]** {task['title']}~~ ✅")
            else:
                col_text.markdown(f"**[{task['subject']}]** {task['title']}")

            # Delete Button
            if col_delete.button("Delete", key=f"del_{task_id}"):
                st.session_state.tasks = [
                    t for t in st.session_state.tasks if t["id"] != task_id
                ]
                st.rerun()

st.divider()
st.caption("my_StudyStack · Built with Streamlit")
