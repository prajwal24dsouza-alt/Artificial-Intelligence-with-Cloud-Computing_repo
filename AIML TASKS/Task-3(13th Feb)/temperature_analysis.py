import numpy as np

# Create numpy array from temperature list (in Celsius)
temperatures = np.array([28, 32, 30, 37, 36, 38])

print("=" * 50)
print("TEMPERATURE ANALYSIS")
print("=" * 50)

# Display the temperature array
print("\nTemperature Data (Celsius):")
print(temperatures)

# Find and print maximum temperature
max_temp = np.max(temperatures)
print(f"\nMaximum Temperature: {max_temp}°C")

# Find and print minimum temperature
min_temp = np.min(temperatures)
print(f"Minimum Temperature: {min_temp}°C")

# Calculate and print average temperature
avg_temp = np.mean(temperatures)
print(f"Average Temperature: {avg_temp}°C")

# Display last 3 days temperature
last_3_days = temperatures[-3:]
print(f"\nLast 3 Days Temperature:")
for i, temp in enumerate(last_3_days, 1):
    print(f"  Day {len(temperatures)-3+i}: {temp}°C")

print("=" * 50)
