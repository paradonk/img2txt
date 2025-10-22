"""
Image Text Extractor using OCR with GUI
Extracts text from images and saves to a text file

Author: Paradorn Katananon
"""

import pytesseract
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading


class ImageToTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Text Extractor")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Variables
        self.current_file = None
        self.current_folder = None

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="📄 Image to Text Extractor",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        # Single Image Button
        self.single_btn = ttk.Button(button_frame, text="📷 Select Single Image",
                                     command=self.select_single_image)
        self.single_btn.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Batch Process Button
        self.batch_btn = ttk.Button(button_frame, text="📁 Select Folder (Batch)",
                                    command=self.select_folder)
        self.batch_btn.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        # About Button
        self.about_btn = ttk.Button(button_frame, text="ℹ️ About",
                                    command=self.show_about)
        self.about_btn.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        # OCR Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="OCR Settings", padding="10")
        settings_frame.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))
        settings_frame.columnconfigure(1, weight=1)

        # Language selection
        ttk.Label(settings_frame, text="Language:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.lang_var = tk.StringVar(value="eng")
        lang_combo = ttk.Combobox(settings_frame, textvariable=self.lang_var,
                                  values=["eng", "chi_sim", "chi_tra", "spa", "fra", "deu", "jpn", "kor"],
                                  state="readonly", width=15)
        lang_combo.grid(row=0, column=1, sticky=tk.W, padx=5)

        # PSM Mode selection
        ttk.Label(settings_frame, text="Page Segmentation:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.psm_var = tk.StringVar(value="6")
        psm_combo = ttk.Combobox(settings_frame, textvariable=self.psm_var,
                                values=["3 (Auto)", "6 (Block)", "11 (Sparse)", "12 (Sparse+OSD)"],
                                state="readonly", width=20)
        psm_combo.grid(row=0, column=3, sticky=tk.W, padx=5)

        # Text Display Frame
        text_frame = ttk.LabelFrame(main_frame, text="Extracted Text Preview", padding="10")
        text_frame.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # Scrolled Text Widget (editable)
        self.text_display = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD,
                                                       width=80, height=20,
                                                       font=('Consolas', 10))
        self.text_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Save Button
        save_button_frame = ttk.Frame(text_frame)
        save_button_frame.grid(row=1, column=0, pady=(5, 0), sticky=(tk.W, tk.E))

        self.save_btn = ttk.Button(save_button_frame, text="💾 Save Text to File",
                                    command=self.save_current_text, state='disabled')
        self.save_btn.pack(side=tk.RIGHT, padx=5)

        self.clear_btn = ttk.Button(save_button_frame, text="🗑️ Clear Text",
                                     command=self.clear_text)
        self.clear_btn.pack(side=tk.RIGHT, padx=5)

        # Status Bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)

        self.status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Progress Bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, pady=(5, 0), sticky=(tk.W, tk.E))

    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def get_psm_value(self):
        """Extract PSM number from combo box value"""
        psm_text = self.psm_var.get()
        return psm_text.split()[0]

    def select_single_image(self):
        """Select and process a single image"""
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.tiff *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.current_file = file_path
            self.process_single_image(file_path)

    def select_folder(self):
        """Select folder for batch processing"""
        folder_path = filedialog.askdirectory(title="Select Folder with Images")

        if folder_path:
            self.current_folder = folder_path
            self.process_folder(folder_path)

    def process_single_image(self, image_path):
        """Process a single image in a separate thread"""
        def process():
            try:
                self.single_btn.config(state='disabled')
                self.batch_btn.config(state='disabled')
                self.progress.start(10)
                self.update_status(f"Processing: {os.path.basename(image_path)}...")

                # Extract text
                text = self.extract_text_from_image(image_path)

                if text:
                    # Display in text widget
                    self.text_display.delete(1.0, tk.END)
                    self.text_display.insert(1.0, text)

                    # Enable save button
                    self.save_btn.config(state='normal')
                    self.current_file = image_path

                    self.update_status(f"✓ Extracted {len(text)} characters from {os.path.basename(image_path)} - Review and edit before saving")
                else:
                    self.update_status("Error: Could not extract text")
                    messagebox.showerror("Error", "Failed to extract text from image")

            except Exception as e:
                self.update_status(f"Error: {str(e)}")
                messagebox.showerror("Error", str(e))
            finally:
                self.progress.stop()
                self.single_btn.config(state='normal')
                self.batch_btn.config(state='normal')

        thread = threading.Thread(target=process, daemon=True)
        thread.start()

    def process_folder(self, folder_path):
        """Process all images in a folder"""
        def process():
            try:
                self.single_btn.config(state='disabled')
                self.batch_btn.config(state='disabled')
                self.progress.start(10)

                # Create output folder
                output_folder = os.path.join(folder_path, "extracted_texts")
                os.makedirs(output_folder, exist_ok=True)

                # Supported formats
                image_extensions = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')

                # Find all images
                image_files = [f for f in os.listdir(folder_path)
                              if f.lower().endswith(image_extensions)]

                if not image_files:
                    self.update_status("No images found in folder")
                    messagebox.showwarning("No Images", "No image files found in the selected folder")
                    return

                self.text_display.delete(1.0, tk.END)
                processed = 0

                for filename in image_files:
                    image_path = os.path.join(folder_path, filename)
                    output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")

                    self.update_status(f"Processing {processed + 1}/{len(image_files)}: {filename}")

                    text = self.extract_text_from_image(image_path, output_file)

                    if text:
                        processed += 1
                        self.text_display.insert(tk.END, f"\n{'='*60}\n")
                        self.text_display.insert(tk.END, f"File: {filename}\n")
                        self.text_display.insert(tk.END, f"Characters: {len(text)}\n")
                        self.text_display.insert(tk.END, f"{'='*60}\n")
                        self.text_display.see(tk.END)

                self.update_status(f"✓ Completed: {processed}/{len(image_files)} images processed")
                messagebox.showinfo("Batch Complete",
                                   f"Processed {processed} images.\nOutput saved to: {output_folder}")

            except Exception as e:
                self.update_status(f"Error: {str(e)}")
                messagebox.showerror("Error", str(e))
            finally:
                self.progress.stop()
                self.single_btn.config(state='normal')
                self.batch_btn.config(state='normal')

        thread = threading.Thread(target=process, daemon=True)
        thread.start()

    def extract_text_from_image(self, image_path, output_file=None):
        """Extract text from an image using OCR"""
        try:
            # Open image
            img = Image.open(image_path)

            # Get settings
            lang = self.lang_var.get()
            psm = self.get_psm_value()

            # Configure OCR
            custom_config = f'--oem 3 --psm {psm}'

            # Extract text
            extracted_text = pytesseract.image_to_string(img, lang=lang, config=custom_config)

            # Save to file if output path provided
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)

            return extracted_text

        except FileNotFoundError:
            raise Exception(f"Image file '{image_path}' not found")
        except Exception as e:
            raise Exception(f"OCR Error: {str(e)}")

    def save_current_text(self):
        """Save the current text in the display (after user review/editing)"""
        # Get current text from display
        current_text = self.text_display.get(1.0, tk.END).strip()

        if not current_text:
            messagebox.showwarning("No Text", "There is no text to save.")
            return

        # Suggest filename based on current file
        if self.current_file:
            default_name = f"{os.path.splitext(os.path.basename(self.current_file))[0]}.txt"
        else:
            default_name = "extracted_text.txt"

        save_path = filedialog.asksaveasfilename(
            title="Save Text File",
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(current_text)
                messagebox.showinfo("Success", f"Text saved to:\n{save_path}")
                self.update_status(f"✓ Saved to: {os.path.basename(save_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

    def clear_text(self):
        """Clear the text display"""
        if self.text_display.get(1.0, tk.END).strip():
            result = messagebox.askyesno("Clear Text", "Are you sure you want to clear the text?")
            if result:
                self.text_display.delete(1.0, tk.END)
                self.save_btn.config(state='disabled')
                self.current_file = None
                self.update_status("Text cleared")

    def show_about(self):
        """Show about dialog with credits"""
        about_text = """Image to Text Extractor

Version: 1.0

An OCR application that extracts text from images
using Tesseract OCR engine.

Created by: Paradorn Katananon

© 2025 All Rights Reserved"""

        messagebox.showinfo("About", about_text)


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = ImageToTextGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
