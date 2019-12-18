def overlap(first_line, second_line):
  first_line_range = set(range(min(first_line), max(first_line) + 1))
  second_line_range = set(range(min(second_line), max(second_line) + 1))
  return bool(first_line_range.intersection(second_line_range))


if __name__ == "__main__":
  x1, x2 = [int(x) for x in input("Enter x1 and x2  value: ").split()]
  x3, x4 = [int(x) for x in input("Enter x3 and x4  value: ").split()]
  
  print(overlap((x1, x2), (x3, x4)))
