import tkinter as tk
from tkinter import messagebox


class DistributedSnapshotSimulator:

    def __init__(self, window):

        self.window = window

        self.window.title("Distributed Snapshot Simulator")
        self.window.geometry("1100x800")
        self.window.configure(bg="#F4F6F8")

        # --------------------------------------------------
        # Processes
        # --------------------------------------------------

        self.processes = [
            "P1",
            "P2",
            "P3",
            "P4"
        ]

        # Local state of each process
        self.process_states = {
            "P1": 0,
            "P2": 0,
            "P3": 0,
            "P4": 0
        }

        # --------------------------------------------------
        # Message channels
        # --------------------------------------------------

        self.channels = {}

        for sender in self.processes:

            for receiver in self.processes:

                if sender != receiver:

                    self.channels[
                        (sender, receiver)
                    ] = []

        # --------------------------------------------------
        # Snapshot variables
        # --------------------------------------------------

        self.snapshot_active = False

        self.snapshot_initiator = None

        self.recorded_states = {}

        self.marker_received = {}

        self.channel_recording = {}

        self.in_transit_messages = {}

        # --------------------------------------------------
        # GUI references
        # --------------------------------------------------

        self.process_state_labels = {}

        # --------------------------------------------------
        # Create interface
        # --------------------------------------------------

        self.create_interface()

    # ======================================================
    # CREATE INTERFACE
    # ======================================================

    def create_interface(self):

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        title = tk.Label(
            self.window,
            text="Distributed Snapshot Simulator",
            font=("Arial", 26, "bold"),
            bg="#F4F6F8",
            fg="#1F2937"
        )

        title.pack(pady=15)

        subtitle = tk.Label(
            self.window,
            text="Chandy–Lamport Distributed Snapshot Algorithm",
            font=("Arial", 13),
            bg="#F4F6F8",
            fg="#6B7280"
        )

        subtitle.pack()

        # --------------------------------------------------
        # Process area
        # --------------------------------------------------

        process_frame = tk.Frame(
            self.window,
            bg="#F4F6F8"
        )

        process_frame.pack(pady=15)

        self.create_process(
            process_frame,
            "P1",
            0,
            0
        )

        self.create_process(
            process_frame,
            "P2",
            0,
            1
        )

        self.create_process(
            process_frame,
            "P3",
            1,
            0
        )

        self.create_process(
            process_frame,
            "P4",
            1,
            1
        )

        # --------------------------------------------------
        # Buttons
        # --------------------------------------------------

        button_frame = tk.Frame(
            self.window,
            bg="#F4F6F8"
        )

        button_frame.pack(pady=10)

        send_button = tk.Button(
            button_frame,
            text="Send Message",
            font=("Arial", 11),
            width=17,
            command=self.open_message_window
        )

        send_button.grid(
            row=0,
            column=0,
            padx=5
        )

        deliver_button = tk.Button(
            button_frame,
            text="Deliver Message",
            font=("Arial", 11),
            width=17,
            command=self.deliver_message
        )

        deliver_button.grid(
            row=0,
            column=1,
            padx=5
        )

        snapshot_button = tk.Button(
            button_frame,
            text="Start Snapshot",
            font=("Arial", 11),
            width=17,
            command=self.start_snapshot
        )

        snapshot_button.grid(
            row=0,
            column=2,
            padx=5
        )

        view_button = tk.Button(
            button_frame,
            text="View Snapshot",
            font=("Arial", 11),
            width=17,
            command=self.view_snapshot
        )

        view_button.grid(
            row=0,
            column=3,
            padx=5
        )

        reset_button = tk.Button(
            button_frame,
            text="Reset",
            font=("Arial", 11),
            width=17,
            command=self.reset_simulator
        )

        reset_button.grid(
            row=0,
            column=4,
            padx=5
        )

        # --------------------------------------------------
        # Event log
        # --------------------------------------------------

        log_title = tk.Label(
            self.window,
            text="Event Log",
            font=("Arial", 16, "bold"),
            bg="#F4F6F8",
            fg="#1F2937"
        )

        log_title.pack(pady=(10, 5))

        self.event_log = tk.Text(
            self.window,
            height=13,
            width=115,
            font=("Courier", 10),
            bg="#1E1E1E",
            fg="white"
        )

        self.event_log.pack(
            padx=20,
            pady=5
        )

        self.add_log(
            "Simulator initialized successfully."
        )

        self.add_log(
            "Ready to simulate distributed messages."
        )

    # ======================================================
    # CREATE PROCESS
    # ======================================================

    def create_process(
        self,
        parent,
        process_name,
        row,
        column
    ):

        frame = tk.Frame(
            parent,
            width=220,
            height=120,
            bg="white",
            highlightbackground="#CBD5E1",
            highlightthickness=2
        )

        frame.grid(
            row=row,
            column=column,
            padx=25,
            pady=10
        )

        frame.pack_propagate(False)

        name_label = tk.Label(
            frame,
            text=process_name,
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#2563EB"
        )

        name_label.pack(pady=10)

        state_label = tk.Label(
            frame,
            text="Local State: 0",
            font=("Arial", 12),
            bg="white",
            fg="#374151"
        )

        state_label.pack()

        self.process_state_labels[
            process_name
        ] = state_label

    # ======================================================
    # SEND MESSAGE WINDOW
    # ======================================================

    def open_message_window(self):

        message_window = tk.Toplevel(
            self.window
        )

        message_window.title(
            "Send Message"
        )

        message_window.geometry(
            "400x350"
        )

        message_window.resizable(
            False,
            False
        )

        title = tk.Label(
            message_window,
            text="Send Message",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=15)

        # Sender

        tk.Label(
            message_window,
            text="Sender:",
            font=("Arial", 12)
        ).pack(pady=3)

        sender = tk.StringVar(
            value="P1"
        )

        sender_menu = tk.OptionMenu(
            message_window,
            sender,
            *self.processes
        )

        sender_menu.config(
            width=15
        )

        sender_menu.pack()

        # Receiver

        tk.Label(
            message_window,
            text="Receiver:",
            font=("Arial", 12)
        ).pack(pady=8)

        receiver = tk.StringVar(
            value="P2"
        )

        receiver_menu = tk.OptionMenu(
            message_window,
            receiver,
            *self.processes
        )

        receiver_menu.config(
            width=15
        )

        receiver_menu.pack()

        # Message

        tk.Label(
            message_window,
            text="Message:",
            font=("Arial", 12)
        ).pack(pady=8)

        message_entry = tk.Entry(
            message_window,
            width=30,
            font=("Arial", 12)
        )

        message_entry.pack()

        # Send

        def send_message():

            sender_process = sender.get()

            receiver_process = receiver.get()

            message = message_entry.get().strip()

            if sender_process == receiver_process:

                messagebox.showerror(
                    "Invalid Message",
                    "Sender and receiver cannot be the same."
                )

                return

            if message == "":

                messagebox.showerror(
                    "Invalid Message",
                    "Please enter a message."
                )

                return

            # Increase sender state
            self.process_states[
                sender_process
            ] += 1

            self.update_process_state(
                sender_process
            )

            # Add message to channel
            self.channels[
                (sender_process, receiver_process)
            ].append({
                "type": "message",
                "sender": sender_process,
                "receiver": receiver_process,
                "text": message
            })

            self.add_log(
                sender_process
                + " → "
                + receiver_process
                + " : "
                + message
                + " [Queued]"
            )

            message_window.destroy()

        send_button = tk.Button(
            message_window,
            text="Send",
            font=("Arial", 12, "bold"),
            width=15,
            command=send_message
        )

        send_button.pack(pady=20)

    # ======================================================
    # DELIVER MESSAGE
    # ======================================================

    def deliver_message(self):

        available_messages = []

        for channel in self.channels:

            queue = self.channels[channel]

            if len(queue) > 0:

                available_messages.append(
                    (
                        channel,
                        queue[0]
                    )
                )

        if len(available_messages) == 0:

            messagebox.showinfo(
                "Message Delivery",
                "No messages are waiting in the channels."
            )

            return

        # Show first waiting message
        channel, message = available_messages[0]

        sender = message["sender"]

        receiver = message["receiver"]

        self.channels[channel].pop(0)

        # --------------------------------------------------
        # Normal message
        # --------------------------------------------------

        if message["type"] == "message":

            self.add_log(
                "Delivered: "
                + sender
                + " → "
                + receiver
                + " : "
                + message["text"]
            )

            # If snapshot is recording this channel,
            # record the message as in-transit.
            if self.snapshot_active:

                key = (
                    sender,
                    receiver
                )

                if self.channel_recording.get(
                    key,
                    False
                ):

                    if key not in self.in_transit_messages:

                        self.in_transit_messages[
                            key
                        ] = []

                    self.in_transit_messages[
                        key
                    ].append(message["text"])

                    self.add_log(
                        "Snapshot recorded in-transit message: "
                        + sender
                        + " → "
                        + receiver
                    )

        # --------------------------------------------------
        # Marker message
        # --------------------------------------------------

        elif message["type"] == "marker":

            self.receive_marker(
                receiver,
                sender
            )

    # ======================================================
    # START SNAPSHOT
    # ======================================================

    def start_snapshot(self):

        if self.snapshot_active:

            messagebox.showinfo(
                "Snapshot",
                "A snapshot is already in progress."
            )

            return

        self.snapshot_active = True

        self.snapshot_initiator = "P1"

        self.recorded_states.clear()

        self.marker_received.clear()

        self.channel_recording.clear()

        self.in_transit_messages.clear()

        self.add_log("")

        self.add_log(
            "========== SNAPSHOT STARTED =========="
        )

        self.add_log(
            "Initiator: P1"
        )

        # Initiator records its state
        self.record_process_state(
            "P1"
        )

        # Send marker to all other processes
        for receiver in self.processes:

            if receiver != "P1":

                self.channels[
                    ("P1", receiver)
                ].append({
                    "type": "marker",
                    "sender": "P1",
                    "receiver": receiver
                })

                self.add_log(
                    "Marker sent: P1 → "
                    + receiver
                )

    # ======================================================
    # RECEIVE MARKER
    # ======================================================

    def receive_marker(
        self,
        receiver,
        sender
    ):

        key = (
            sender,
            receiver
        )

        # First marker received
        if receiver not in self.marker_received:

            self.marker_received[
                receiver
            ] = True

            self.record_process_state(
                receiver
            )

            self.add_log(
                receiver
                + " received first marker from "
                + sender
            )

            # Start recording incoming channels
            for process in self.processes:

                if process != receiver:

                    channel_key = (
                        process,
                        receiver
                    )

                    self.channel_recording[
                        channel_key
                    ] = True

            # Send markers to other processes
            for process in self.processes:

                if process != receiver:

                    self.channels[
                        (receiver, process)
                    ].append({
                        "type": "marker",
                        "sender": receiver,
                        "receiver": process
                    })

                    self.add_log(
                        "Marker sent: "
                        + receiver
                        + " → "
                        + process
                    )

        else:

            # Marker closes a recording channel
            self.channel_recording[
                key
            ] = False

            self.add_log(
                "Marker received: "
                + sender
                + " → "
                + receiver
                + " | Channel recording stopped"
            )

        # Check whether snapshot is complete
        self.check_snapshot_complete()

    # ======================================================
    # RECORD PROCESS STATE
    # ======================================================

    def record_process_state(
        self,
        process
    ):

        if process in self.recorded_states:

            return

        self.recorded_states[
            process
        ] = self.process_states[
            process
        ]

        self.add_log(
            process
            + " local state recorded: "
            + str(
                self.process_states[
                    process
                ]
            )
        )

    # ======================================================
    # CHECK SNAPSHOT COMPLETION
    # ======================================================

    def check_snapshot_complete(self):

        if len(
            self.recorded_states
        ) == len(self.processes):

            self.snapshot_active = False

            self.add_log(
                "========== SNAPSHOT COMPLETE =========="
            )

            self.add_log(
                "All process states have been recorded."
            )

    # ======================================================
    # VIEW SNAPSHOT
    # ======================================================

    def view_snapshot(self):

        if len(
            self.recorded_states
        ) == 0:

            messagebox.showinfo(
                "Global Snapshot",
                "No snapshot has been recorded yet."
            )

            return

        result = ""

        result += (
            "GLOBAL SNAPSHOT\n"
        )

        result += (
            "==============================\n\n"
        )

        result += (
            "Recorded Process States\n"
        )

        result += (
            "------------------------------\n"
        )

        for process in self.processes:

            if process in self.recorded_states:

                result += (
                    process
                    + " → Local State: "
                    + str(
                        self.recorded_states[
                            process
                        ]
                    )
                    + "\n"
                )

        result += "\n"

        result += (
            "In-Transit Messages\n"
        )

        result += (
            "------------------------------\n"
        )

        found_message = False

        for channel in self.in_transit_messages:

            messages = self.in_transit_messages[
                channel
            ]

            for message in messages:

                found_message = True

                result += (
                    channel[0]
                    + " → "
                    + channel[1]
                    + " : "
                    + message
                    + "\n"
                )

        if not found_message:

            result += (
                "No in-transit messages recorded.\n"
            )

        result += "\n"

        result += (
            "Snapshot Status: "
            + (
                "COMPLETE"
                if not self.snapshot_active
                else "IN PROGRESS"
            )
        )

        messagebox.showinfo(
            "Global Snapshot",
            result
        )

    # ======================================================
    # UPDATE PROCESS STATE
    # ======================================================

    def update_process_state(
        self,
        process
    ):

        state = self.process_states[
            process
        ]

        self.process_state_labels[
            process
        ].config(
            text="Local State: "
            + str(state)
        )

    # ======================================================
    # ADD LOG
    # ======================================================

    def add_log(
        self,
        message
    ):

        self.event_log.insert(
            tk.END,
            message
            + "\n"
        )

        self.event_log.see(
            tk.END
        )

    # ======================================================
    # RESET
    # ======================================================

    def reset_simulator(self):

        for process in self.processes:

            self.process_states[
                process
            ] = 0

            self.update_process_state(
                process
            )

        for channel in self.channels:

            self.channels[
                channel
            ].clear()

        self.snapshot_active = False

        self.snapshot_initiator = None

        self.recorded_states.clear()

        self.marker_received.clear()

        self.channel_recording.clear()

        self.in_transit_messages.clear()

        self.event_log.delete(
            "1.0",
            tk.END
        )

        self.add_log(
            "Simulator reset successfully."
        )


# ==========================================================
# MAIN PROGRAM
# ==========================================================

window = tk.Tk()

app = DistributedSnapshotSimulator(
    window
)

window.mainloop()