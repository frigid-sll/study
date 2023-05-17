package main

import (
	"fmt"
	"os"
)

func main() {
	var name string
	var age int
	var height float64
	fmt.Fprintln(os.Stdout, "Please enter your name, age and height:")
	n, err := fmt.Fscanf(os.Stdin, "%s %d %f", &name, &age, &height)
	if err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		return
	}
	fmt.Fprintf(os.Stdout, "Name: %s\nAge: %d\nHeight: %.2f\n", name, age, height)
	fmt.Fprintf(os.Stdout, "Successfully read %d parameters.\n", n)
}
