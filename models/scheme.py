from marshmallow import Schema, fields
from marshmallow.validate import OneOf, Length, Regexp


class UserScheme(Schema):
    first_name = fields.Str(required=True, validate=Length(min=3, max=255))
    last_name = fields.Str(required=True, validate=Length(min=3, max=255))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(min=10, max=255))
    phone = fields.Str(
        required=True,
        validate=[
            Length(min=10, max=14),
            Regexp(regex="^([0|\+[0-9]{1,5})?([7-9][0-9]{9})$"),
        ],
    )
    dob = fields.Date(required=True)
    gender = fields.Str(required=True, validate=OneOf(["M", "F", "O"]))
    address = fields.Str(required=True, validate=Length(min=3, max=255))
    role = fields.Int(required=True)


class LoginScheme(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(min=10, max=255))


class MusicScheme(Schema):
    user_id = fields.Int(required=True)
    title = fields.Str(required=True, validate=Length(min=3, max=255))
    album_name = fields.Str(required=True, validate=Length(min=3, max=255))
    genre = fields.Str(
        required=True, validate=OneOf(["country", "classic", "rock", "jazz"])
    )


class UserUpdateScheme(Schema):
    first_name = fields.Str(required=True, validate=Length(min=3, max=255))
    last_name = fields.Str(required=True, validate=Length(min=3, max=255))
    phone = fields.Str(
        required=True,
        validate=[
            Length(min=10, max=14),
            Regexp(regex="^([0|\+[0-9]{1,5})?([7-9][0-9]{9})$"),
        ],
    )
    dob = fields.Date(required=True)
    gender = fields.Str(required=True, validate=OneOf(["M", "F", "O"]))
    address = fields.Str(required=True, validate=Length(min=3, max=255))


class MusicUpdateScheme(Schema):
    title = fields.Str(required=True, validate=Length(min=3, max=255))
    album_name = fields.Str(required=True, validate=Length(min=3, max=255))
    genre = fields.Str(
        required=True, validate=OneOf(["country", "classic", "rock", "jazz"])
    )
