function main(path)
    println("hello world")
    println("solution 2")
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
