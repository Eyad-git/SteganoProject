def gcd(a, b):
    """Helper to find Greatest Common Divisor without importing math."""
    while b:
        a, b = b, a % b
    return a

class StepGenerator:
    def __init__(self, password, total_pixels):
        """
        Calculates a Start Index and a Step Size based on the password.
        Ensures the Step is 'coprime' to total_pixels so we visit unique spots.
        """
        self.total = total_pixels
        self.password_val = self._string_to_int(password)
        
        # 1. Calculate Start Position (0 to total-1)
        self.start = self.password_val % total_pixels
        
        # 2. Calculate Step Size
        # We want a large step so bits are scattered far apart.
        # We start with a base step derived from the password.
        base_step = (self.password_val // total_pixels) + (total_pixels // 2)
        
        # Ensure step is coprime to total (GCD is 1)
        # If GCD != 1, we increment until it is.
        while gcd(base_step, total_pixels) != 1:
            base_step += 1
            
        self.step = base_step

    def _string_to_int(self, s):
        """Turns password string into a large integer."""
        if not s: return 123456789
        h = 0
        for char in s:
            h = (31 * h + ord(char)) & 0xFFFFFFFF
        return h

    def get_index(self, i):
        """
        Returns the pixel index for the i-th bit of the message.
        Formula: (Start + (i * Step)) % Total
        Computation is O(1) - Instant.
        """
        return (self.start + (i * self.step)) % self.total