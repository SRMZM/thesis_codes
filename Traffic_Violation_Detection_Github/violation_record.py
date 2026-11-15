# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 14:55:58 2026

@author: Russell
"""

# -*- coding: utf-8 -*-

"""
Store and manage vehicle violation records.
"""


class ViolationRecord:

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(
            self,
            track_id,
            plate=None,
            entry_side=None,
            exit_side=None,
            movement=None,
            violation=False,
            violation_type=None,
            entry_frame=None,
            #violation_frame=None,
            exit_frame=None,
            entry_timestamp=None,
            violation_timestamp=None,
            exit_timestamp=None,
            date=None,
            time=None
        ):

        # Store vehicle tracking ID.
        self.track_id = track_id

        # Store license plate.
        self.plate = plate

        # Store intersection entry side.
        self.entry_side = entry_side

        # Store intersection exit side.
        self.exit_side = exit_side
        
        # Store vehicle movement.
        self.movement = movement

        # Store whether a violation occurred.
        self.violation = violation

        # Store violation type.
        self.violation_type = violation_type

        # Store important frame numbers.
        self.entry_frame = entry_frame
        #self.violation_frame = violation_frame
        self.exit_frame = exit_frame

        # Store timestamps inside the video.
        self.entry_timestamp = entry_timestamp
        self.violation_timestamp = violation_timestamp
        self.exit_timestamp = exit_timestamp

        # Store real date and time if available.
        self.date = date
        self.time = time


    # =====================================================
    # Convert record to dictionary
    # =====================================================

    def to_dict(self):

        return {
            "track_id": self.track_id,

            "plate": self.plate,

            "entry_side": self.entry_side,
            "exit_side": self.exit_side,
            
            "movement": self.movement,

            "violation": self.violation,
            "violation_type": self.violation_type,

            "entry_frame": self.entry_frame,
            #"violation_frame": self.violation_frame,
            "exit_frame": self.exit_frame,

            "entry_timestamp": self.entry_timestamp,
            "violation_timestamp": self.violation_timestamp,
            "exit_timestamp": self.exit_timestamp,

            "date": self.date,
            "time": self.time
        }


    # =====================================================
    # String representation
    # =====================================================

    def __str__(self):

        return (
            f"Vehicle ID: {self.track_id} | "
            f"Plate: {self.plate} | "
            f"Entry: {self.entry_side} | "
            f"Exit: {self.exit_side} | "
            f"Violation: {self.violation}"
        )
    
    
class ViolationRecordManager:

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(self):

        # Store records using track ID as the key.
        self.records = {}


    # =====================================================
    # Create a record
    # =====================================================

    def create_record(
            self,
            track_id
        ):

        # Do not create duplicate records.
        if track_id in self.records:

            return self.records[track_id]


        # Create a new record.
        record = ViolationRecord(
            track_id=track_id
        )


        # Store the record.
        self.records[track_id] = record


        return record


    # =====================================================
    # Get a record
    # =====================================================

    def get_record(
            self,
            track_id
        ):

        return self.records.get(
            track_id
        )


    # =====================================================
    # Get all records
    # =====================================================

    def get_all_records(self):

        return list(
            self.records.values()
        )