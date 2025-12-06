# Backward Reasoner - Sub-Goal Handling Issue

**Date**: 2025-12-05
**Status**: 6/13 tests passing, working on sub-goal recursion

## Current State

The backward reasoner has 80% coverage and passes simple tests:
- ✅ Basic instantiation
- ✅ Simple goal (symmetry)
- ✅ Already known facts
- ✅ Unprovable goals
- ✅ Multiple independent goals
- ❌ **Goals requiring sub-goal proving (transitivity)** ← FAILING

## Failing Test

`test_prove_with_subgoals` - Tests proving `AB = EF` from `AB = CD` and `CD = EF` using transitivity.

**Theorem**: `AB = CD, CD = EF => AB = EF`
**Known facts**: `AB = CD`, `CD = EF`
**Goal**: `AB = EF`

**Expected**: Success (should apply transitivity since both conditions are known)
**Actual**: Failure (goal not proven)

## Root Cause Analysis

The current backward reasoning algorithm:

```python
while iteration < max_iterations:
    # Select goal
    current_goal = select_goal(state)

    # Find theorems that could prove goal
    applicable_theorems = find_theorems_for_goal(current_goal, state)

    # Get first theorem and its sub-goals (conditions)
    theorem, sub_goals = applicable_theorems[0]

    # Check if sub-goals are all satisfied
    if all(state.has_fact(sg) for sg in sub_goals):
        # All sub-goals satisfied, derive goal
        state.add_fact(current_goal)
        state.remove_goal(current_goal)
    else:
        # Add unsatisfied sub-goals to goal queue
        for sub_goal in sub_goals:
            if not state.has_fact(sub_goal):
                state.add_goal(sub_goal)
```

**The algorithm looks correct** - it should:
1. Find that transitivity can prove `AB = EF`
2. Check sub-goals: `AB = CD`, `CD = EF`
3. Both are already facts
4. Derive `AB = EF`

## Debugging Needed

Need to add debug output to understand why the test fails:
1. Are applicable theorems being found?
2. Are sub-goals being correctly instantiated?
3. Are sub-goals matching the known facts?

## Possible Issues

1. **Fact equality**: Maybe `EqualSegment(AB, CD)` created in the test doesn't equal the `EqualSegment(AB, CD)` instantiated from the pattern
2. **Parameter ordering**: Conditions might have swapped parameter order
3. **Unifier issue**: Pattern substitution might not be working correctly

## Next Steps

1. Create debug script for transitivity test
2. Check if sub-goals match known facts exactly
3. Add debug output to backward reasoner
4. Fix the issue
5. Run remaining tests (7 more)

## Files

- **Implementation**: `geometry_prover/proof/backward_reasoner.py` (108 lines, 80% coverage)
- **Tests**: `tests/test_proof/test_backward_reasoner.py` (13 tests, 6 passing)
- **Debug**: `/tmp/debug_backward_reasoner.py`
