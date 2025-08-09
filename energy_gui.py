# energy_gui.py

import tkinter as tk
from tkinter import messagebox
import energy_input     # Import functions from energy_input.py
import energy_processor # Import functions from energy_processor.py


class EnergyPredictorApp:
    def __init__(self, master):
        self.master = master
        master.title("Smart Home Energy Predictor 🏡💡")
        master.geometry("800x700")
        master.resizable(True, True)

        # Configure main window layout
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(0, weight=0)  # Appliances input
        master.grid_rowconfigure(1, weight=0)  # Appliance list
        master.grid_rowconfigure(2, weight=1, minsize=150)  # Household & Weather section
        master.grid_rowconfigure(3, weight=0)  # Button
        master.grid_rowconfigure(4, weight=1)  # Results

        self.api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # <--- Replace with your API key

        # --- Appliance Input Section ---
        self.appliance_frame = tk.LabelFrame(master, text="Add Appliances", padx=10, pady=10)
        self.appliance_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.appliance_frame.grid_columnconfigure(1, weight=1)

        tk.Label(self.appliance_frame, text="Appliance Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self.appliance_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(self.appliance_frame, text="Wattage (W/unit):").grid(row=1, column=0, sticky="w")
        self.wattage_entry = tk.Entry(self.appliance_frame)
        self.wattage_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(self.appliance_frame, text="Daily Hours Used (h/unit):").grid(row=2, column=0, sticky="w")
        self.hours_entry = tk.Entry(self.appliance_frame)
        self.hours_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(self.appliance_frame, text="Quantity:").grid(row=3, column=0, sticky="w")
        self.quantity_entry = tk.Entry(self.appliance_frame)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        tk.Button(self.appliance_frame, text="Add Appliance", command=self.add_appliance).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        # --- Appliance List ---
        self.appliance_list_frame = tk.LabelFrame(master, text="Added Appliances", padx=10, pady=10)
        self.appliance_list_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.appliance_listbox = tk.Listbox(self.appliance_list_frame, height=6)
        self.appliance_listbox.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(self.appliance_list_frame, orient="vertical", command=self.appliance_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.appliance_listbox.config(yscrollcommand=scrollbar.set)

        tk.Button(self.appliance_list_frame, text="Remove Selected", command=self.remove_appliance).pack(pady=5)

        self.appliances_data = []

        # --- Household & Weather Info ---
        self.config_frame = tk.LabelFrame(master, text="Household & Weather Info", padx=10, pady=10)
        self.config_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.config_frame.grid_columnconfigure(1, weight=1)
        self.config_frame.grid_rowconfigure(0, weight=0)
        self.config_frame.grid_rowconfigure(1, weight=0)

        tk.Label(self.config_frame, text="Home Size (sqft):").grid(row=0, column=0, sticky="w")
        self.home_size_entry = tk.Entry(self.config_frame)
        self.home_size_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(self.config_frame, text="City for Weather:").grid(row=1, column=0, sticky="w")
        self.city_entry = tk.Entry(self.config_frame)
        self.city_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Prevent shrinking
        self.config_frame.configure(height=120)
        self.config_frame.grid_propagate(False)

        # --- Predict Button ---
        tk.Button(master, text="Calculate Energy Prediction", command=self.run_prediction,
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).grid(
            row=3, column=0, columnspan=2, pady=15, padx=10, sticky="ew"
        )

        # --- Results ---
        self.results_frame = tk.LabelFrame(master, text="Prediction Results", padx=10, pady=10)
        self.results_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.results_text = tk.Text(self.results_frame, height=10, wrap="word", state="disabled", font=("Courier New", 10))
        self.results_text.pack(fill="both", expand=True)
        results_scrollbar = tk.Scrollbar(self.results_frame, orient="vertical", command=self.results_text.yview)
        results_scrollbar.pack(side="right", fill="y")
        self.results_text.config(yscrollcommand=results_scrollbar.set)

    def add_appliance(self):
        try:
            appliance_info = energy_input.validate_and_get_appliance_data(
                self.name_entry.get(),
                self.wattage_entry.get(),
                self.hours_entry.get(),
                self.quantity_entry.get()
            )
            self.appliances_data.append(appliance_info)
            self.update_appliance_listbox()
            self.clear_appliance_entries()
        except ValueError as e:
            messagebox.showwarning("Input Error", str(e))

    def remove_appliance(self):
        try:
            selected_index = self.appliance_listbox.curselection()[0]
            del self.appliances_data[selected_index]
            self.update_appliance_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select an appliance to remove.")

    def update_appliance_listbox(self):
        self.appliance_listbox.delete(0, tk.END)
        for i, app in enumerate(self.appliances_data):
            self.appliance_listbox.insert(tk.END,
                f"{i+1}. {app['quantity']}x {app['name']} ({app['wattage']}W, {app['hours_of_use']}h/day)")

    def clear_appliance_entries(self):
        self.name_entry.delete(0, tk.END)
        self.wattage_entry.delete(0, tk.END)
        self.hours_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, "1")

    def run_prediction(self):
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)

        # Household data
        try:
            household_data = energy_input.validate_and_get_household_data(self.home_size_entry.get())
        except ValueError as e:
            messagebox.showwarning("Input Error", f"Household Info: {str(e)}")
            self.results_text.insert(tk.END, f"Warning: {str(e)}\n\n")
            household_data = {}

        # Weather data
        city = self.city_entry.get()
        is_api_key_valid = energy_input.validate_api_key(self.api_key)

        if not city:
            self.results_text.insert(tk.END, "Warning: City not provided for weather data.\n\n")
            weather_data = {'city': 'N/A', 'temperature': 'N/A', 'humidity': 'N/A', 'description': 'N/A'}
        elif not is_api_key_valid:
            try:
                temp_input = messagebox.askstring("Simulated Temperature", f"Enter simulated temp (°C) for {city}:")
                simulated_temp = float(temp_input) if temp_input else 'N/A'
                weather_data = {'city': city, 'temperature': simulated_temp, 'humidity': 'N/A', 'description': 'N/A'}
            except ValueError:
                weather_data = {'city': city, 'temperature': 'N/A', 'humidity': 'N/A', 'description': 'N/A'}
        else:
            try:
                weather_data = energy_processor.fetch_weather_data(city, self.api_key)
            except Exception as e:
                messagebox.showerror("Weather API Error", str(e))
                weather_data = {'city': city, 'temperature': 'N/A', 'humidity': 'N/A', 'description': 'N/A'}

        # Prediction
        results_text, total_kwh = energy_processor.predict_daily_total_energy(
            self.appliances_data, household_data, weather_data
        )
        self.results_text.insert(tk.END, results_text)
        self.results_text.config(state="disabled")

        messagebox.showinfo("Prediction Complete", f"Total daily energy: {total_kwh:.2f} kWh")


def main():
    root = tk.Tk()
    app = EnergyPredictorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
