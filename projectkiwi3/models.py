from pydantic import BaseModel
from typing import List, Optional
import json


# model Imagery {
#   id             Int                    @id @default(autoincrement())
#   sub            String
#   name           String
#   projectId      Int
#   createdAt      DateTime               @default(now())
#   ready          Boolean                @default(false)
#   error          Boolean                @default(false)
#   project        Project                @relation(fields: [projectId], references: [id], onDelete: Cascade)
#   storageSizeKB  Int?
#   labelingQueues LabelingQueueImagery[]
#   modifiedAt DateTime @default(now())
#   reconstruction ReconstructionEntry?
# }

class Imagery(BaseModel):
    id: int
    sub: str
    name: str
    createdAt: str
    ready: bool
    error: bool
    storageSizeKB: Optional[int]
    modifiedAt: str
    
    @classmethod
    def from_dict(cls, data: dict):

        return cls(
            id = data['id'],
            sub = data['sub'],
            name = data['name'],
            createdAt = data['createdAt'],
            ready = data['ready'],
            error = data['error'],
            storageSizeKB = data['storageSizeKB'],
            modifiedAt = data['modifiedAt'],
        )
    

# model LabelingTask {
#   id              Int              @id @default(autoincrement())
#   labelingQueueId Int
#   complete        Boolean          @default(false)
#   completedBy     String?
#   labelingQueue   LabelingQueue    @relation(fields: [labelingQueueId], references: [id], onDelete: Cascade)
#   taskCoordinates TaskCoordinate[]
# }
class LabelingTask(BaseModel):

    id: int
    complete: bool
    completedBy: Optional[str]
    coordinates: List[List[float]] # [[lng, lat], [lng,lat]]

    @classmethod
    def from_dict(cls, data: dict):
        coords = []
        for coord in data['taskCoordinates']:
            coords.append([coord['lng'], coord['lat']])
        return cls(
            id = data['id'],
            complete = data['complete'],
            completedBy = data['completedBy'],
            coordinates = coords
        )
    
    
    

# model LabelingQueue {
#   id                   Int                    @id @default(autoincrement())
#   name                 String?
#   projectId            Int
#   createdBy            String
#   project              Project                @relation(fields: [projectId], references: [id], onDelete: Cascade)
#   labelingQueueImagery LabelingQueueImagery[]
#   labelingTasks        LabelingTask[]
#   modifiedAt DateTime @default(now())
# }
class LabelingQueue(BaseModel):

    id: int
    name: Optional[str] = None
    createdBy: str
    modifiedAt: str
    labelingTasks: List[LabelingTask]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id = data['id'],
            name = data['name'],
            createdBy = data['createdBy'],
            modifiedAt = data['modifiedAt'],
            labelingTasks = [LabelingTask.from_dict(dict) for dict in data['labelingTasks']]
        )
    






# model Label {
#   id          Int          @id @default(autoincrement())
#   name        String
#   color       String
#   projectId   Int
#   active      Boolean      @default(true)
#   annotations Annotation[]
#   project     Project      @relation(fields: [projectId], references: [id], onDelete: Cascade)
#   modifiedAt DateTime @default(now())
# }
class Label(BaseModel):

    id: int
    name: str
    color: str
    active: bool
    modifiedAt: str
    

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id = data['id'],
            name = data['name'],
            color = data['color'],
            active = data['active'],
            modifiedAt = data['modifiedAt']
        )


# model Annotation {
#   id          Int          @id @default(autoincrement())
#   sub         String
#   projectId   Int
#   shape       String
#   createdAt   DateTime     @default(now())
#   confidence  Float        @default(1)
#   labelId     Int
#   label       Label        @relation(fields: [labelId], references: [id], onDelete: Cascade)
#   project     Project      @relation(fields: [projectId], references: [id], onDelete: Cascade)
#   coordinates Coordinate[]
#   modifiedAt DateTime @default(now())
# }
class Annotation(BaseModel):

    id: int
    sub: str
    shape: str
    createdAt: str
    confidence: float
    labelId: int
    label: Label
    modifiedAt: str
    coordinates: List[List[float]] # [[lng, lat], [lng,lat]]


    @classmethod
    def from_dict(cls, data: dict):
        coords = []
        for coord in data['coordinates']:
            coords.append([coord['lng'], coord['lat']])
        return cls(
            id = data['id'],
            sub = data['sub'],
            shape = data['shape'],
            createdAt = data['createdAt'],
            confidence = data['confidence'],
            labelId = data['labelId'],
            label = Label.from_dict(data['label']),
            modifiedAt = data['modifiedAt'],
            coordinates = coords
        )


class AnnotationPayload(BaseModel):
    coordinates: List[List[float]]
    shape: str
    labelId: int
    confidence: float

    def toJSON(self):
        return {
                'coordinates': self.coordinates,
                'shape': self.shape,
                'labelId': self.labelId,
                'confidence': self.confidence
            }

    
# model Project {
#   id              Int              @id @default(autoincrement())
#   name            String
#   createdAt       DateTime         @default(now())
#   owner           String
#   annotations     Annotation[]
#   deletedAnnotations DeletedAnnotation[]
#   images          Image[]
#   deletedImages DeletedImage[]
#   imagery         Imagery[]
#   deletedImagery DeletedImagery[]
#   labels          Label[]
#   labelingQueues  LabelingQueue[]
#   previousProject MigratedProject?
#   members         ProjectMember[]
#   projectShares   ProjectShare[]
#   modifiedAt DateTime @default(now())
# }
class Project(BaseModel):

    id: int
    name: str
    createdAt: str
    modifiedAt: str
    owner: str
    labels: Optional[List[Label]] = None


    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id = data['id'],
            name = data['name'],
            createdAt = data['createdAt'],
            modifiedAt = data['modifiedAt'],
            owner = data['owner'],
            labels = [Label.from_dict(labelDict) for labelDict in data['labels']] \
                    if 'labels' in data else None
        )
