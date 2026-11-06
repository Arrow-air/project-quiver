---
title: Flight Test Campaign Payment Mechanics
sidebar_label: Flight Test Campaign Payments
sidebar_position: 4
---

# Flight Test Campaign Payment Mechanics, V1

V1 for task T-17 (#263), drafted 2026-10-29 and adopted by the Project Lead on 2026-11-05. It is revised on team feedback (section 10). Governs the 10,000 $ARROW Flight Test Campaign pool approved in April 2026 and held on the Project Quiver multisig.

## 1. What the pool pays for

People who fly a Quiver and put the evidence where the project can use it. The pool pays for validated flights and for milestones, in $ARROW, from the multisig, in the monthly batch. It does not pay for aircraft time, fuel, travel or parts. It is not a retainer and it is not a bounty.

## 2. A validated flight

A flight counts when all four hold:

1. The dataflash log is on the flight tracking platform (flights.arrowair.com) and has parsed.
2. The flight record is filled: title, start time, aircraft, pilot, the intent of the flight and what happened, tags, and the campaign or test card it belongs to if any.
3. The aircraft left the ground and landed under control. Ground runs, tethered runs and aborted takeoffs are not flights.
4. Someone other than the pilot has read the record against the log and marked it validated in the platform notes or the task issue. Default reviewer: Zeynep for the lead's flights, the lead for everyone else's. The reviewer can be anyone on the core team if the default is unavailable.

A flight that reaches a planned end state is validated. An endurance flight flown to the battery low stage ends on a battery message by design and counts.

## 3. The rate

| Flight type | $ARROW |
|---|---|
| Campaign flight. A flight flown against a written test card or task matrix with a defined deliverable (obstacle avoidance cards, the endurance matrix, an attachment test, a replication flight like T-13) | 300 per validated flight |
| Free flight. Any validated flight that is not part of a defined campaign | 10 per logged minute, from 5 minutes up, to a maximum of 150 per flight |

Free flights pay for airtime, not for takeoffs.

- A free flight under 5 minutes pays nothing. A hover and land earns no reward.
- The rate tops out at 150 $ARROW, which a 15 minute flight reaches.
- An operator is paid for at most two free flights per day. Further flights that day still count toward milestones.
- Duration is the flight duration the platform parses from the log.

The rates are fixed in $ARROW, not converted from a dollar figure, because the pool is denominated in $ARROW. 300 $ARROW is about one hour at the $48 call time rate the monthly retro uses, at the $0.16 conversion used in September. A campaign flight with its preparation, upload and record is about an hour of operator work beyond the flying.

## 4. Milestones

Milestones reward the things the flight record is short of. Each one is paid once per operator unless the table says otherwise, on top of the flight's own pay, and is read from the platform record.

| Milestone | $ARROW | How it is met |
|---|---|---|
| First flight | 300 | The operator's first validated flight on a Quiver |
| First hour | 300 | 60 minutes of validated airtime in total |
| Ten clean flights | 500 | Ten validated flights in a row, each 5 minutes or longer, with no incident on the platform record |
| Twenty minutes | 300 | One validated flight of 20 minutes or longer |
| Endurance record | 1,000 | The longest validated flight on a Quiver, beating the standing record by at least one minute. The record to beat is 25.2 minutes (2026-09-01, Houston unit, no payload). The pack and payload are stated with every record. Paid once per record |
| First autonomous mission | 300 | A mission of two or more waypoints flown in AUTO to completion with no pilot takeover |
| First heavy payload | 300 | A validated flight carrying 5 kg or more, with the weighed mass in the record |
| First wind flight | 300 | A validated flight with mean wind above 5 m/s measured at the site and written in the record. It must stay inside the Pilot's Handbook limit of 15 knots sustained and 18 knots in gusts |
| New site | 150 | The first validated flight at a site that is not yet on the platform. Paid once per site, to the first operator who logs it |
| Failure report | 150 | A problem report filed through the Handbook reporting path with the log attached, accepted by the lead as a real and new failure. Paid per distinct failure. A crash or an unplanned failsafe earns no flight pay (section 5), and this bonus is why it is still worth uploading |

Rules for milestones:

- They count from 2026-11-05. A milestone an operator reached before that date is not paid.
- The retained lead does not draw milestones.
- No milestone pays for a flight outside the Pilot's Handbook limits. A record set by ignoring a battery stage, a wind limit, or a geofence is not a record.

## 5. What is excluded

- Flights already paid under a bounty or a priced task. The QGB-02 avoidance campaign flights are paid through QGB-02 and draw nothing here.
- Flights by the retained lead that are inside the retainer's own operations: bench checks, hover checks after maintenance, configuration flights, demonstrations. Campaign flights by the lead with a defined deliverable are included, which is the T-03 case.
- A flight that ends in a crash, or in a failsafe action the pilot did not plan for (an unplanned RTL, a forced landing, a kill switch event). The failure report milestone in section 4 covers the report, not the flight.
- Ferry hops and repositioning.
- Campaign flights under 60 seconds airborne, unless the test card defines a shorter flight. Free flights under 5 minutes (section 3).
- Flights flown before 2026-10-01. Earlier flights were flown under the monthly retainers or paid under a bounty.

## 6. The cap

One operator can draw at most 2,500 $ARROW from the pool in a phase (a three month funding period). That is a quarter of the pool. Flight pay and milestones both count toward it. The cap exists because the proposal promised the DAO that most of the pool would remain for operators who join as the dev kit fleet grows. The pool balance and the draws to date are published in every monthly progress report.

## 7. The clock

Computed monthly with the retro nominations, from the platform record as of the last day of the month. Paid in the same CSV airdrop batch as the retro, listed on its own row in the report's $ARROW table so campaign pay and retro are never mixed. The lead computes, the reviewer of record for each flight is named in the computation, and the GBC second signature on the batch is the check.

## 8. Operator onboarding

The $1,500 USDC operator onboarding fund earmarked in QGB-FLEX is separate from this pool. It covers the one time costs of bringing a new operator in (travel to a build, a transmitter, a first set of spares) and is drawn by the lead's decision, not by flights.

## 9. First computations

**T-13, Julius, 2026-10-02.** One replication flight flown against the T-13 task (switches installed, TCP session live), a 28 second hover, validated by the lead on 2026-10-27 from the raw logs. The flight is under the 60 second floor in section 5 and shorter than the few minutes the task asked for. It was flown and accepted before these mechanics existed, so the lead pays it once at the campaign rate as a stated exception. The exception does not carry to any later flight. One campaign flight: 300 $ARROW. Paid in the November batch.

**T-03, the endurance matrix, Erick.** Six flights, no payload, 5 kg and 7 kg, each as a hover and as the AUTO figure 8, flown at the ranch in November against the matrix on #250. Validated when KBM confirms the six logs are usable for the study. Six campaign flights: 1,800 $ARROW, inside the 2,500 cap for the phase. Paid in the batch after KBM's confirmation.

Pool after both: 10,000 minus 2,100 = 7,900 $ARROW.

## 10. Changes

The Project Lead adopted V1 on 2026-11-05 without a team vote and revises it on team feedback. Every change is recorded in the wiki notes with its date, applies from the next month, and never applies to flights already flown. V2 is written when a second operator has flown ten validated flights, which is the first real test of the cap, the milestones and the reviewer rule.
