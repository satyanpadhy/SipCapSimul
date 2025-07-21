import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scapy.all import *
from scapy.layers.inet import IP
from difflib import SequenceMatcher
import json

class PCAPCompare:
    def __init__(self, root):
        self.root = root
        self.root.title('PCAP SIP Comparator')
        self.root.geometry('1200x800')

        # Configure styles
        style = ttk.Style()
        style.configure('Toolbar.TFrame', background='#f0f0f0')
        style.configure('Content.TFrame', background='white')
        style.configure('Header.TLabel', font=('TkDefaultFont', 10, 'bold'))
        style.configure('Accent.TButton', background='#007bff', foreground='white')
        style.configure('Filter.TLabelframe', background='white')
        style.configure('Treeview', background='white', fieldbackground='white', foreground='black')
        style.configure('Treeview.Heading', font=('TkDefaultFont', 9, 'bold'))
        style.map('Treeview',
                  background=[('selected', '#007bff')],
                  foreground=[('selected', 'white')])
        
        # Configure PanedWindow style
        style.configure('TPanedwindow', background='#e0e0e0')
        style.configure('TPanedwindow.Sash', 
                       sashthickness=4,
                       sashrelief='raised',
                       background='#c0c0c0',
                       borderwidth=1)
        style.map('TPanedwindow.Sash',
                  background=[('pressed', '#808080'), ('active', '#a0a0a0')])

        # Variables
        self.pcap1_path = tk.StringVar()
        self.pcap2_path = tk.StringVar()
        self.pcap1_messages = []
        self.pcap2_messages = []

        self.setup_ui()
        
        # Configure tags for highlighting
        self.tree1.tag_configure('different', background='#fff3cd')
        self.tree2.tag_configure('different', background='#fff3cd')

        # Configure text widget tags
        self.text1.tag_configure('highlight', background='#fff3cd')
        self.text2.tag_configure('highlight', background='#fff3cd')
        self.text1.tag_configure('header', font=('TkDefaultFont', 9, 'bold'))
        self.text2.tag_configure('header', font=('TkDefaultFont', 9, 'bold'))

    def setup_ui(self):
        # Create main toolbar frame with styling
        toolbar = ttk.Frame(self.root, style='Toolbar.TFrame')
        toolbar.pack(fill=tk.X, padx=10, pady=5)

        # File operations frame (left side of toolbar)
        file_frame = ttk.LabelFrame(toolbar, text="File Operations", padding="10", style='Filter.TLabelframe')
        file_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # PCAP 1 frame
        pcap1_frame = ttk.Frame(file_frame)
        pcap1_frame.pack(fill=tk.X, pady=3)
        ttk.Label(pcap1_frame, text="PCAP 1:", width=8, style='Header.TLabel').pack(side=tk.LEFT)
        ttk.Entry(pcap1_frame, textvariable=self.pcap1_path, width=40, font=('TkDefaultFont', 9)).pack(side=tk.LEFT, padx=2)
        ttk.Button(pcap1_frame, text="Browse", width=8, command=lambda: self.browse_file(self.pcap1_path)).pack(side=tk.LEFT, padx=2)

        # PCAP 2 frame
        pcap2_frame = ttk.Frame(file_frame)
        pcap2_frame.pack(fill=tk.X, pady=3)
        ttk.Label(pcap2_frame, text="PCAP 2:", width=8, style='Header.TLabel').pack(side=tk.LEFT)
        ttk.Entry(pcap2_frame, textvariable=self.pcap2_path, width=40, font=('TkDefaultFont', 9)).pack(side=tk.LEFT, padx=2)
        ttk.Button(pcap2_frame, text="Browse", width=8, command=lambda: self.browse_file(self.pcap2_path)).pack(side=tk.LEFT, padx=2)

        # Load button with accent style
        ttk.Button(file_frame, text="Load and Compare", command=self.load_and_compare, style='Accent.TButton').pack(pady=5)

        # Filter frame (right side of toolbar)
        filter_frame = ttk.LabelFrame(toolbar, text="Filters", padding="10", style='Filter.TLabelframe')
        filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Message type filter
        type_frame = ttk.Frame(filter_frame)
        type_frame.pack(fill=tk.X, pady=3)
        ttk.Label(type_frame, text="Type:", width=8, style='Header.TLabel').pack(side=tk.LEFT)
        self.message_type = tk.StringVar(value="ALL")
        message_types = ["ALL", "INVITE", "ACK", "BYE", "CANCEL", "OPTIONS", "REGISTER", "200 OK", "4XX", "5XX", "6XX"]
        self.type_filter = ttk.Combobox(type_frame, textvariable=self.message_type, values=message_types, width=15, font=('TkDefaultFont', 9))
        self.type_filter.pack(side=tk.LEFT, padx=2)

        # Call-ID filter
        callid_frame = ttk.Frame(filter_frame)
        callid_frame.pack(fill=tk.X, pady=3)
        ttk.Label(callid_frame, text="Call-ID:", width=8, style='Header.TLabel').pack(side=tk.LEFT)
        self.search_callid = tk.StringVar()
        ttk.Entry(callid_frame, textvariable=self.search_callid, width=25, font=('TkDefaultFont', 9)).pack(side=tk.LEFT, padx=2)

        # Apply filter button with accent style
        ttk.Button(filter_frame, text="Apply Filters", command=self.apply_filters, style='Accent.TButton').pack(pady=5)

        # Main content frame with PanedWindow for resizable split views
        content_frame = ttk.Frame(self.root, style='Content.TFrame')
        content_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Horizontal PanedWindow for side-by-side view
        h_paned = ttk.PanedWindow(content_frame, orient=tk.HORIZONTAL)
        h_paned.grid(row=0, column=0, sticky='nsew')

        # Left side container
        left_container = ttk.Frame(h_paned)
        left_container.grid_rowconfigure(0, weight=1)
        left_container.grid_columnconfigure(0, weight=1)
        h_paned.add(left_container, weight=1)

        # Right side container
        right_container = ttk.Frame(h_paned)
        right_container.grid_rowconfigure(0, weight=1)
        right_container.grid_columnconfigure(0, weight=1)
        h_paned.add(right_container, weight=1)

        # Left vertical PanedWindow
        left_paned = ttk.PanedWindow(left_container, orient=tk.VERTICAL)
        left_paned.grid(row=0, column=0, sticky='nsew')

        # Right vertical PanedWindow
        right_paned = ttk.PanedWindow(right_container, orient=tk.VERTICAL)
        right_paned.grid(row=0, column=0, sticky='nsew')

        # PCAP 1 Message List Frame
        list_frame1 = ttk.Frame(left_paned)
        left_paned.add(list_frame1, weight=3)
        ttk.Label(list_frame1, text="PCAP 1 Messages", style='Header.TLabel').pack(anchor="w", pady=(0, 5), padx=5)

        # PCAP 1 Treeview with scrollbars in a container
        tree1_container = ttk.Frame(list_frame1)
        tree1_container.pack(fill=tk.BOTH, expand=True)
        tree1_container.grid_columnconfigure(0, weight=1)
        tree1_container.grid_rowconfigure(0, weight=1)

        self.tree1 = ttk.Treeview(tree1_container, columns=('Time', 'Type', 'Message'), show='headings')
        self.tree1.heading('Time', text='Time')
        self.tree1.heading('Type', text='Type')
        self.tree1.heading('Message', text='Message')
        self.tree1.column('Time', width=150)
        self.tree1.column('Type', width=100)
        self.tree1.column('Message', width=400)
        tree1_scroll_y = ttk.Scrollbar(tree1_container, orient=tk.VERTICAL, command=self.tree1.yview)
        tree1_scroll_x = ttk.Scrollbar(tree1_container, orient=tk.HORIZONTAL, command=self.tree1.xview)
        self.tree1.configure(yscrollcommand=tree1_scroll_y.set, xscrollcommand=tree1_scroll_x.set)

        self.tree1.grid(row=0, column=0, sticky="nsew")
        tree1_scroll_y.grid(row=0, column=1, sticky="ns")
        tree1_scroll_x.grid(row=1, column=0, sticky="ew")

        # PCAP 1 Message Details Frame
        detail_frame1 = ttk.Frame(left_paned)
        left_paned.add(detail_frame1, weight=2)
        ttk.Label(detail_frame1, text="PCAP 1 Message Details", style='Header.TLabel').pack(anchor="w", pady=(0, 5), padx=5)

        # PCAP 1 Text with scrollbars in a container
        text1_container = ttk.Frame(detail_frame1)
        text1_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text1_container.grid_columnconfigure(0, weight=1)
        text1_container.grid_rowconfigure(0, weight=1)

        self.text1 = tk.Text(text1_container, wrap=tk.NONE, font=('TkDefaultFont', 9),
                            bg='white', relief='solid', borderwidth=1)
        text1_scroll_y = ttk.Scrollbar(text1_container, orient=tk.VERTICAL, command=self.text1.yview)
        text1_scroll_x = ttk.Scrollbar(text1_container, orient=tk.HORIZONTAL, command=self.text1.xview)
        self.text1.configure(yscrollcommand=text1_scroll_y.set, xscrollcommand=text1_scroll_x.set)

        self.text1.grid(row=0, column=0, sticky="nsew")
        text1_scroll_y.grid(row=0, column=1, sticky="ns")
        text1_scroll_x.grid(row=1, column=0, sticky="ew")

        # PCAP 2 Message List Frame
        list_frame2 = ttk.Frame(right_paned)
        right_paned.add(list_frame2, weight=3)
        ttk.Label(list_frame2, text="PCAP 2 Messages", style='Header.TLabel').pack(anchor="w", pady=(0, 5), padx=5)

        # PCAP 2 Treeview with scrollbars in a container
        tree2_container = ttk.Frame(list_frame2)
        tree2_container.pack(fill=tk.BOTH, expand=True)
        tree2_container.grid_columnconfigure(0, weight=1)
        tree2_container.grid_rowconfigure(0, weight=1)

        self.tree2 = ttk.Treeview(tree2_container, columns=('Time', 'Type', 'Message'), show='headings')
        self.tree2.heading('Time', text='Time')
        self.tree2.heading('Type', text='Type')
        self.tree2.heading('Message', text='Message')
        self.tree2.column('Time', width=150)
        self.tree2.column('Type', width=100)
        self.tree2.column('Message', width=400)
        tree2_scroll_y = ttk.Scrollbar(tree2_container, orient=tk.VERTICAL, command=self.tree2.yview)
        tree2_scroll_x = ttk.Scrollbar(tree2_container, orient=tk.HORIZONTAL, command=self.tree2.xview)
        self.tree2.configure(yscrollcommand=tree2_scroll_y.set, xscrollcommand=tree2_scroll_x.set)

        self.tree2.grid(row=0, column=0, sticky="nsew")
        tree2_scroll_y.grid(row=0, column=1, sticky="ns")
        tree2_scroll_x.grid(row=1, column=0, sticky="ew")

        # PCAP 2 Message Details Frame
        detail_frame2 = ttk.Frame(right_paned)
        right_paned.add(detail_frame2, weight=2)
        ttk.Label(detail_frame2, text="PCAP 2 Message Details", style='Header.TLabel').pack(anchor="w", pady=(0, 5), padx=5)

        # PCAP 2 Text with scrollbars in a container
        text2_container = ttk.Frame(detail_frame2)
        text2_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


        self.text2 = tk.Text(text2_container, wrap=tk.NONE, font=('TkDefaultFont', 9),
                            bg='white', relief='solid', borderwidth=1)
        text2_scroll_y = ttk.Scrollbar(text2_container, orient=tk.VERTICAL, command=self.text2.yview)
        text2_scroll_x = ttk.Scrollbar(text2_container, orient=tk.HORIZONTAL, command=self.text2.xview)
        self.text2.configure(yscrollcommand=text2_scroll_y.set, xscrollcommand=text2_scroll_x.set)

        self.text2.grid(row=0, column=0, sticky="nsew")
        text2_scroll_y.grid(row=0, column=1, sticky="ns")
        text2_scroll_x.grid(row=1, column=0, sticky="ew")
        text2_container.grid_columnconfigure(0, weight=1)
        text2_container.grid_rowconfigure(0, weight=1)

        self.text2 = tk.Text(text2_container, wrap=tk.WORD, font=('TkDefaultFont', 9),
                            bg='white', relief='solid', borderwidth=1)
        text2_scroll = ttk.Scrollbar(text2_container, orient=tk.VERTICAL, command=self.text2.yview)
        self.text2.configure(yscrollcommand=text2_scroll.set)

        self.text2.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        text2_scroll.grid(row=0, column=1, sticky="ns")

        # Configure tree columns
        for tree in (self.tree1, self.tree2):
            tree.heading('Time', text='Time')
            tree.heading('Message', text='Message')
            tree.column('Time', width=100)
            tree.column('Message', width=400)

        # Bind selection events
        self.tree1.bind('<<TreeviewSelect>>', self.show_message_details1)
        self.tree2.bind('<<TreeviewSelect>>', self.show_message_details2)

    def browse_file(self, path_var):
        filename = filedialog.askopenfilename(filetypes=[("PCAP files", "*.pcap")])
        if filename:
            path_var.set(filename)

    def apply_filters(self):
        # Clear current display
        for tree in [self.tree1, self.tree2]:
            for item in tree.get_children():
                tree.delete(item)
        
        # Apply filters to both PCAP message lists
        self.display_filtered_messages(self.pcap1_messages, self.tree1)
        self.display_filtered_messages(self.pcap2_messages, self.tree2)
        
        # Reapply difference highlighting
        self.highlight_differences()
    
    def display_filtered_messages(self, messages, tree):
        for i, msg in enumerate(messages):
            if self.filter_message(msg):
                tree.insert('', 'end', f"I{i+1}", values=(f"{msg['time']:.6f}", f"{msg['first_line']} (Call-ID: {msg['call_id']})"))
    
    def filter_message(self, msg):
        # Check message type filter
        msg_type = self.message_type.get()
        if msg_type != "ALL":
            if msg_type in ["4XX", "5XX", "6XX"]:
                # Check response code range
                first_word = msg['first_line'].split()[0]
                if first_word.isdigit():
                    code = int(first_word)
                    if msg_type == "4XX" and not (400 <= code <= 499):
                        return False
                    if msg_type == "5XX" and not (500 <= code <= 599):
                        return False
                    if msg_type == "6XX" and not (600 <= code <= 699):
                        return False
            elif msg_type not in msg['first_line']:
                return False
        
        # Check Call-ID filter
        callid_filter = self.search_callid.get().strip()
        if callid_filter and callid_filter not in msg['call_id']:
            return False
        
        return True

    def extract_sip_messages(self, pcap_path):
        messages = []
        try:
            packets = rdpcap(pcap_path)
            for packet in packets:
                if UDP in packet and Raw in packet:
                    try:
                        raw_data = packet[Raw].load.decode('utf-8', errors='ignore')
                        if 'SIP/2.0' in raw_data:
                            # Parse SIP message to get method/status and Call-ID
                            first_line = raw_data.split('\n')[0].strip()
                            call_id = ''
                            for line in raw_data.split('\n'):
                                if 'Call-ID:' in line:
                                    call_id = line.split('Call-ID:')[1].strip()
                                    break
                            
                            messages.append({
                                'time': packet.time,
                                'message': raw_data,
                                'first_line': first_line,
                                'call_id': call_id
                            })
                    except Exception as e:
                        print(f"Error processing packet: {str(e)}")
                        continue
        except Exception as e:
            messagebox.showerror("Error", f"Error reading PCAP file: {str(e)}")
        return messages

    def compare_messages(self, msg1, msg2):
        # First compare Call-IDs if available
        if msg1['call_id'] and msg2['call_id'] and msg1['call_id'] == msg2['call_id']:
            return True
        
        # If Call-IDs don't match or aren't available, compare first lines and content
        first_line_ratio = SequenceMatcher(None, msg1['first_line'], msg2['first_line']).ratio()
        content_ratio = SequenceMatcher(None, msg1['message'], msg2['message']).ratio()
        
        # Weight the comparison (give more weight to first line)
        weighted_ratio = (first_line_ratio * 0.6) + (content_ratio * 0.4)
        return weighted_ratio > 0.8  # Threshold for similarity

    def highlight_differences(self):
        # Clear previous highlights
        for item in self.tree1.get_children():
            self.tree1.item(item, tags=())
        for item in self.tree2.get_children():
            self.tree2.item(item, tags=())

        # Compare and highlight differences
        for i, msg1 in enumerate(self.pcap1_messages):
            found_match = False
            for j, msg2 in enumerate(self.pcap2_messages):
                if self.compare_messages(msg1, msg2):
                    found_match = True
                    break
            if not found_match:
                self.tree1.item(f"I{i+1}", tags=('different',))

        for i, msg2 in enumerate(self.pcap2_messages):
            found_match = False
            for j, msg1 in enumerate(self.pcap1_messages):
                if self.compare_messages(msg2, msg1):
                    found_match = True
                    break
            if not found_match:
                self.tree2.item(f"I{i+1}", tags=('different',))

    def highlight_text_differences(self, text1, text2):
        """Compare two texts and return lists of difference indices."""
        import difflib
        d = difflib.Differ()
        diff = list(d.compare(text1.splitlines(True), text2.splitlines(True)))
        
        text1_ranges = []
        text2_ranges = []
        pos1 = pos2 = 0
        
        for line in diff:
            if line.startswith('  '):  # Common line
                pos1 += len(line[2:])
                pos2 += len(line[2:])
            elif line.startswith('- '):  # Line unique to text1
                start = pos1
                pos1 += len(line[2:])
                text1_ranges.append((start, pos1))
            elif line.startswith('+ '):  # Line unique to text2
                start = pos2
                pos2 += len(line[2:])
                text2_ranges.append((start, pos2))
        
        return text1_ranges, text2_ranges

    def show_message_details1(self, event):
        selection = self.tree1.selection()
        if selection:
            item = selection[0]
            index = int(item[1:]) - 1
            if 0 <= index < len(self.pcap1_messages):
                self.text1.delete(1.0, tk.END)
                msg1 = self.pcap1_messages[index]['message']
                self.text1.insert(tk.END, msg1)
                
                # If there's a selection in tree2, compare and highlight differences
                tree2_selection = self.tree2.selection()
                if tree2_selection:
                    tree2_index = int(tree2_selection[0][1:]) - 1
                    if 0 <= tree2_index < len(self.pcap2_messages):
                        msg2 = self.pcap2_messages[tree2_index]['message']
                        ranges1, _ = self.highlight_text_differences(msg1, msg2)
                        
                        # Clear existing tags
                        self.text1.tag_remove('different', '1.0', tk.END)
                        
                        # Apply highlighting to differences
                        for start, end in ranges1:
                            start_index = '1.0 + %d chars' % start
                            end_index = '1.0 + %d chars' % end
                            self.text1.tag_add('different', start_index, end_index)
                        
                # Configure the difference highlighting style
                self.text1.tag_configure('different', background='yellow')

    def show_message_details2(self, event):
        selection = self.tree2.selection()
        if selection:
            item = selection[0]
            index = int(item[1:]) - 1
            if 0 <= index < len(self.pcap2_messages):
                self.text2.delete(1.0, tk.END)
                msg2 = self.pcap2_messages[index]['message']
                self.text2.insert(tk.END, msg2)
                
                # If there's a selection in tree1, compare and highlight differences
                tree1_selection = self.tree1.selection()
                if tree1_selection:
                    tree1_index = int(tree1_selection[0][1:]) - 1
                    if 0 <= tree1_index < len(self.pcap1_messages):
                        msg1 = self.pcap1_messages[tree1_index]['message']
                        _, ranges2 = self.highlight_text_differences(msg1, msg2)
                        
                        # Clear existing tags
                        self.text2.tag_remove('different', '1.0', tk.END)
                        
                        # Apply highlighting to differences
                        for start, end in ranges2:
                            start_index = '1.0 + %d chars' % start
                            end_index = '1.0 + %d chars' % end
                            self.text2.tag_add('different', start_index, end_index)
                        
                # Configure the difference highlighting style
                self.text2.tag_configure('different', background='yellow')

    def load_and_compare(self):
        # Load messages from both PCAPs
        self.pcap1_messages = self.extract_sip_messages(self.pcap1_path.get())
        self.pcap2_messages = self.extract_sip_messages(self.pcap2_path.get())

        # Apply filters and display messages
        self.apply_filters()

        messagebox.showinfo("Load Complete", 
            f"Loaded {len(self.pcap1_messages)} messages from PCAP 1\n" +
            f"Loaded {len(self.pcap2_messages)} messages from PCAP 2\n\n" +
            "Use the filters above to narrow down the messages.")

def main():
    root = tk.Tk()
    app = PCAPCompare(root)
    root.mainloop()

if __name__ == "__main__":
    main()