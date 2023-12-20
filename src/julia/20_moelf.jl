const ON, OFF = true, false
const HIGH, LOW = true, false

abstract type ElfModule end

function Base.push!(src::ElfModule, dest::ElfModule)
    push!(src.dest_modules, dest)
end

function connect!(src::ElfModule, dests::Vector{<:ElfModule})
    for dest in dests
        push!(src, dest)
    end
end

struct Pulse
    origin::String
    shape::Bool
    function Pulse(origin, shape)
        if shape == HIGH
            HI_COUNT[] += 1
        else
            LO_COUNT[] += 1
        end
        return new(origin, shape)
    end
end

@kwdef mutable struct Sink <: ElfModule
    name::String
    input_queue::Vector{Pulse} = Pulse[]
    dest_modules::Vector{ElfModule} = ElfModule[]
end
pulse!(m::Sink, _) = popfirst!(m.input_queue)

@kwdef mutable struct FlipFlop <: ElfModule
    name::String
    state::Bool = OFF
    input_queue::Vector{Pulse} = Pulse[]
    dest_modules::Vector{ElfModule} = ElfModule[]
end
function pulse!(m::FlipFlop, QUEUE)
    in_pulse = popfirst!(m.input_queue)
    if in_pulse.shape == HIGH
    else
        m.state = !m.state
        for dest in m.dest_modules
            out_pulse = Pulse(m.name, m.state)
            push!(QUEUE, dest)
            push!(dest.input_queue, out_pulse)
        end
    end
end

@kwdef mutable struct Conjunction <: ElfModule
    name::String
    input_queue::Vector{Pulse} = Pulse[]
    source_modules::Vector{ElfModule} = ElfModule[]
    source_mem::Dict{String,Bool} = Dict(x.name => LOW for x in source_modules)
    source_mem_seen::Dict{String,Int} = Dict(x.name => -1 for x in source_modules)
    dest_modules::Vector{ElfModule} = ElfModule[]
    is_feed::Bool = false
end
function Base.push!(src::ElfModule, dest::Conjunction)
    push!(src.dest_modules, dest)
    dest.source_mem[src.name] = LOW
    dest.source_mem_seen[src.name] = 0
end

function pulse!(m::Conjunction, QUEUE)
    in_pulse = popfirst!(m.input_queue)
    m.source_mem[in_pulse.origin] = in_pulse.shape
    if m.is_feed && in_pulse.shape == HIGH
        seen = m.source_mem_seen
        from = in_pulse.origin
        seen[from] += 1
        if !haskey(CYCLE_DICT, from)
            CYCLE_DICT[from] = BUTTON_COUNT[]
        end
    end
    for dest in m.dest_modules
        out_pulse = if all(==(HIGH), values(m.source_mem))
            Pulse(m.name, LOW)
        else
            Pulse(m.name, HIGH)
        end
        push!(QUEUE, dest)
        push!(dest.input_queue, out_pulse)
    end
end

@kwdef mutable struct Broadcaster <: ElfModule
    name::String
    input_queue::Vector{Pulse} = Pulse[]
    dest_modules::Vector{ElfModule} = ElfModule[]
end
function pulse!(m::Broadcaster, QUEUE)
    in_pulse = popfirst!(m.input_queue)
    for dest in m.dest_modules
        out_pulse = Pulse(m.name, in_pulse.shape)
        push!(QUEUE, dest)
        push!(dest.input_queue, out_pulse)
    end
end

function make_modules(lines)
    ms = Dict{String,ElfModule}()
    for (left, _) in lines
        if left == "broadcaster"
            ms[left] = Broadcaster(; name=left)
        else
            prefix, name... = left
            if prefix == '%'
                ms[name] = FlipFlop(; name)
            elseif prefix == '&'
                ms[name] = Conjunction(; name)
            end
        end
    end
    return ms
end

function make_connections!(All_ElfModules, lines)
    for (left, right) in lines
        names = split(right, ", ")
        ms = ElfModule[]
        for n in names
            if haskey(All_ElfModules, n)
                push!(ms, All_ElfModules[n])
            else
                s = Sink(name=n)
                All_ElfModules[n] = s
                push!(ms, s)
            end
        end
        if left == "broadcaster"
            connect!(All_ElfModules[left], ms)
        else
            prefix, name... = left
            connect!(All_ElfModules[name], ms)
        end
    end
end

function button!(All_ElfModules, QUEUE)
    b = All_ElfModules["broadcaster"]
    push!(b.input_queue, Pulse("button", LOW))
    push!(QUEUE, b)
end

const HI_COUNT, LO_COUNT = Ref(0), Ref(0)
const BUTTON_COUNT = Ref(0)
const CYCLE_DICT = Dict{String,Int}()

function main(path)
    lines = split.(readlines(path), " -> ")
    All_ElfModules = make_modules(lines)
    make_connections!(All_ElfModules, lines)

    QUEUE = ElfModule[]
    rx = All_ElfModules["rx"]
    feed = only(v for (k,v) in All_ElfModules if rx ∈ v.dest_modules)
    feed.is_feed = true

    while true
        BUTTON_COUNT[] += 1
        button!(All_ElfModules, QUEUE)
        while !isempty(QUEUE)
            m = popfirst!(QUEUE)
            pulse!(m, QUEUE)
        end
        if BUTTON_COUNT[] == 1000
            println(HI_COUNT[]* LO_COUNT[])
        end
        if all(>(0), values(feed.source_mem_seen))
            println(lcm(values(CYCLE_DICT)...))
            break
        end
    end
end

(abspath(PROGRAM_FILE) == @__FILE__) && main(ARGS[1])
